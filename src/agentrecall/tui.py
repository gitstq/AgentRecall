"""
Terminal UI dashboard for AgentRecall using rich-like formatting.
Provides an interactive dashboard for browsing and managing memories.
"""

import os
import sys
import time
import json
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class TUIDashboard:
    """Terminal UI dashboard for AgentRecall."""

    CATEGORY_COLORS = {
        "architecture": Colors.CYAN,
        "decision": Colors.YELLOW,
        "bug": Colors.RED,
        "feature": Colors.GREEN,
        "config": Colors.MAGENTA,
        "context": Colors.BLUE,
        "general": Colors.WHITE,
        "tech_stack": Colors.CYAN,
        "api": Colors.YELLOW,
        "performance": Colors.GREEN,
        "security": Colors.RED,
        "workflow": Colors.MAGENTA,
        "lesson": Colors.BLUE,
    }

    CATEGORY_ICONS = {
        "architecture": "🏗️",
        "decision": "🎯",
        "bug": "🐛",
        "feature": "✨",
        "config": "⚙️",
        "context": "📋",
        "general": "📝",
        "tech_stack": "🔧",
        "api": "🔗",
        "performance": "⚡",
        "security": "🔒",
        "workflow": "🔄",
        "lesson": "💡",
    }

    def __init__(self, store, search_engine):
        self.store = store
        self.search = search_engine
        self.width = self._get_terminal_width()

    def _get_terminal_width(self) -> int:
        """Get terminal width, default to 80."""
        try:
            return os.get_terminal_size().columns
        except (OSError, ValueError):
            return 80

    def _print_header(self, title: str, subtitle: str = ""):
        """Print a styled header."""
        width = self.width
        print()
        print(f"{Colors.BOLD}{Colors.CYAN}{'─' * width}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}  🧠 {title}{Colors.RESET}")
        if subtitle:
            print(f"{Colors.DIM}  {subtitle}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'─' * width}{Colors.RESET}")
        print()

    def _print_separator(self, char: str = "─"):
        """Print a separator line."""
        print(f"{Colors.DIM}{char * self.width}{Colors.RESET}")

    def _truncate(self, text: str, max_len: int) -> str:
        """Truncate text with ellipsis."""
        if len(text) <= max_len:
            return text
        return text[:max_len - 3] + "..."

    def _format_time(self, timestamp: float) -> str:
        """Format timestamp to readable string."""
        if not timestamp:
            return "N/A"
        dt = time.localtime(timestamp)
        now = time.localtime()
        diff = time.mktime(now) - timestamp

        if diff < 60:
            return f"{int(diff)}s ago"
        elif diff < 3600:
            return f"{int(diff / 60)}m ago"
        elif diff < 86400:
            return f"{int(diff / 3600)}h ago"
        elif diff < 604800:
            return f"{int(diff / 86400)}d ago"
        else:
            return time.strftime("%Y-%m-%d", dt)

    def _importance_bar(self, importance: float) -> str:
        """Create a visual importance bar."""
        filled = int(importance * 10)
        empty = 10 - filled
        color = Colors.GREEN if importance >= 0.7 else Colors.YELLOW if importance >= 0.4 else Colors.RED
        return f"{color}{'█' * filled}{'░' * empty}{Colors.RESET} {importance:.1f}"

    def _category_style(self, category: str) -> str:
        """Get styled category string with icon and color."""
        icon = self.CATEGORY_ICONS.get(category, "📝")
        color = self.CATEGORY_COLORS.get(category, Colors.WHITE)
        return f"{color}{icon} {category.upper()}{Colors.RESET}"

    def show_dashboard(self, agent_id: str = "default"):
        """Show the main dashboard overview."""
        self._print_header("AgentRecall Dashboard",
                          f"Agent: {agent_id}")

        # Stats
        stats = self.store.get_stats(agent_id)
        categories = self.store.get_categories(agent_id)

        print(f"  {Colors.BOLD}📊 Statistics{Colors.RESET}")
        print(f"  {Colors.CYAN}  Total Memories:{Colors.RESET}    {Colors.BOLD}{stats['total_memories']}{Colors.RESET}")
        print(f"  {Colors.CYAN}  Categories:{Colors.RESET}        {Colors.BOLD}{stats['categories']}{Colors.RESET}")
        print(f"  {Colors.CYAN}  Sessions:{Colors.RESET}          {Colors.BOLD}{stats['sessions']}{Colors.RESET}")
        print(f"  {Colors.CYAN}  Avg Importance:{Colors.RESET}    {Colors.BOLD}{stats['avg_importance']}{Colors.RESET}")
        print(f"  {Colors.CYAN}  Total Accesses:{Colors.RESET}    {Colors.BOLD}{stats['total_accesses']}{Colors.RESET}")
        print()

        # Category breakdown
        if categories:
            print(f"  {Colors.BOLD}📂 Categories{Colors.RESET}")
            max_cat_len = max(len(c["category"]) for c in categories[:8])
            for cat in categories[:8]:
                name = cat["category"].ljust(max_cat_len + 2)
                count = cat["count"]
                avg_imp = cat["avg_importance"] or 0
                bar = "█" * min(count, 30)
                print(f"  {self._category_style(cat['category'])}  "
                      f"{Colors.DIM}{count:>4}{Colors.RESET}  "
                      f"{Colors.GREEN}{bar}{Colors.RESET}  "
                      f"{Colors.DIM}avg:{avg_imp:.1f}{Colors.RESET}")
            print()

        # Recent memories
        recent = self.store.get_recent(agent_id, limit=5)
        if recent:
            print(f"  {Colors.BOLD}🕐 Recent Memories{Colors.RESET}")
            self._print_separator()
            for mem in recent:
                self._print_memory_row(mem)
            self._print_separator()

        print()

    def show_memory_detail(self, memory_id: int):
        """Show detailed view of a single memory."""
        mem = self.store.get_memory(memory_id)
        if not mem:
            print(f"{Colors.RED}  Memory #{memory_id} not found.{Colors.RESET}")
            return

        self._print_header(f"Memory #{mem['id']}", mem['title'])

        print(f"  {Colors.BOLD}Category:{Colors.RESET}     {self._category_style(mem['category'])}")
        print(f"  {Colors.BOLD}Importance:{Colors.RESET}   {self._importance_bar(mem['importance'])}")
        print(f"  {Colors.BOLD}Access Count:{Colors.RESET} {mem['access_count']}")
        print(f"  {Colors.BOLD}Created:{Colors.RESET}      {self._format_time(mem['created_at'])}")
        print(f"  {Colors.BOLD}Updated:{Colors.RESET}      {self._format_time(mem['updated_at'])}")
        print(f"  {Colors.BOLD}Session:{Colors.RESET}      {mem.get('session_id', 'N/A')}")

        tags = mem.get('tags', [])
        if tags:
            tags_str = " ".join(f"{Colors.CYAN}[{t}]{Colors.RESET}" for t in tags)
            print(f"  {Colors.BOLD}Tags:{Colors.RESET}         {tags_str}")

        print()
        self._print_separator()
        print(f"  {Colors.BOLD}Content:{Colors.RESET}")
        print()

        # Word-wrap content
        content = mem['content']
        width = self.width - 4
        words = content.split()
        line = ""
        for word in words:
            if len(line) + len(word) + 1 <= width:
                line = f"{line} {word}" if line else word
            else:
                print(f"  {Colors.DIM}{line}{Colors.RESET}")
                line = word
        if line:
            print(f"  {Colors.DIM}{line}{Colors.RESET}")

        print()
        self._print_separator()

        # Related memories
        related = self.search.suggest_related(memory_id, limit=3)
        if related:
            print(f"  {Colors.BOLD}🔗 Related Memories{Colors.RESET}")
            for r in related:
                score = r.get("_score", 0)
                print(f"  {Colors.DIM}  #{r['id']}{Colors.RESET} "
                      f"{Colors.BOLD}{self._truncate(r['title'], 50)}{Colors.RESET} "
                      f"{Colors.GREEN}(score: {score:.2f}){Colors.RESET}")
            print()

    def show_search_results(self, results: list, query: str = ""):
        """Display search results."""
        if query:
            self._print_header("Search Results", f'Query: "{query}"')
        else:
            self._print_header("Memories")

        if not results:
            print(f"  {Colors.YELLOW}  No memories found.{Colors.RESET}")
            print()
            return

        print(f"  {Colors.DIM}Found {len(results)} result(s){Colors.RESET}")
        print()
        self._print_separator()
        for mem in results:
            self._print_memory_row(mem, show_score=True)
        self._print_separator()
        print()

    def show_context_preview(self, context: str, agent_id: str):
        """Preview the context that would be injected to an agent."""
        self._print_header("Context Preview", f"Agent: {agent_id}")

        if not context:
            print(f"  {Colors.YELLOW}  No context available.{Colors.RESET}")
            print()
            return

        lines = context.split("\n")
        for line in lines:
            if line.startswith("#"):
                print(f"  {Colors.BOLD}{Colors.CYAN}{line}{Colors.RESET}")
            elif line.startswith("["):
                print(f"  {Colors.BOLD}{Colors.GREEN}{line}{Colors.RESET}")
            else:
                print(f"  {Colors.DIM}{line}{Colors.RESET}")
        print()

    def show_agents(self):
        """Display all registered agents."""
        self._print_header("Registered Agents")
        agents = self.store.get_all_agents()

        if not agents:
            print(f"  {Colors.YELLOW}  No agents registered yet.{Colors.RESET}")
            print()
            return

        for agent in agents:
            print(f"  {Colors.BOLD}{Colors.CYAN}🤖 {agent['name']}{Colors.RESET}")
            print(f"     {Colors.DIM}ID: {agent['id']}{Colors.RESET}")
            desc = agent.get('description', '')
            if desc:
                print(f"     {Colors.DIM}{desc}{Colors.RESET}")
            print(f"     {Colors.DIM}Memories: {agent['total_memories']} | "
                  f"Last active: {self._format_time(agent['last_active'])}{Colors.RESET}")
            print()

    def show_categories(self, agent_id: str = "default"):
        """Display category breakdown."""
        self._print_header("Categories", f"Agent: {agent_id}")
        categories = self.store.get_categories(agent_id)

        if not categories:
            print(f"  {Colors.YELLOW}  No categories found.{Colors.RESET}")
            print()
            return

        print(f"  {'Category':<20} {'Count':>8} {'Avg Imp':>10}")
        self._print_separator()
        for cat in categories:
            print(f"  {self._category_style(cat['category']):<20} "
                  f"{cat['count']:>8} "
                  f"{cat['avg_importance'] or 0:>10.2f}")
        print()

    def show_export(self, content: str, format_type: str):
        """Display exported content."""
        self._print_header(f"Export ({format_type.upper()})")
        print(content)
        print()

    def _print_memory_row(self, mem: dict, show_score: bool = False):
        """Print a single memory as a table row."""
        mem_id = mem.get("id", "?")
        title = self._truncate(mem.get("title", "Untitled"), 40)
        category = mem.get("category", "general")
        importance = mem.get("importance", 0.5)
        updated = self._format_time(mem.get("updated_at", 0))
        access = mem.get("access_count", 0)

        parts = [
            f"  {Colors.DIM}#{mem_id:<5}{Colors.RESET}",
            f"{self._category_style(category)}",
            f"{Colors.BOLD}{title}{Colors.RESET}",
            f"{self._importance_bar(importance)}",
            f"{Colors.DIM}{updated}{Colors.RESET}",
        ]

        if show_score:
            score = mem.get("_score", mem.get("relevance_score", 0))
            parts.append(f"{Colors.GREEN}score:{score:.2f}{Colors.RESET}")

        if access > 0:
            parts.append(f"{Colors.DIM}hits:{access}{Colors.RESET}")

        print(" ".join(parts))
