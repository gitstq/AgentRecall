"""
AgentRecall CLI - Main entry point.
Lightweight AI Coding Agent Persistent Memory Engine.

Usage:
    recall save --title "..." --content "..." [--category decision] [--tags tag1,tag2]
    recall search "query" [--mode hybrid] [--category ...] [--limit 20]
    recall show <id>
    recall list [--category ...] [--limit 20]
    recall delete <id>
    recall update <id> [--title ...] [--content ...] [--importance ...]
    recall dashboard [--agent ...]
    recall context [--agent ...] [--max-tokens 4000]
    recall session start [--agent ...] [--description ...]
    recall session end [--summary ...]
    recall session history [--agent ...]
    recall export [--format json|markdown] [--output file]
    recall import <file> [--agent ...]
    recall stats [--agent ...]
    recall agents
    recall categories [--agent ...]
    recall cleanup [--max-age-days 90] [--min-importance 0.3]
    recall compress <id>
    recall suggest <id>
"""

import sys
import os
import argparse
import json
import time

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agentrecall.store import MemoryStore
from agentrecall.search import SearchEngine
from agentrecall.compressor import MemoryCompressor
from agentrecall.session import SessionManager
from agentrecall.tui import TUIDashboard, Colors
from agentrecall import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="recall",
        description="🧠 AgentRecall - Lightweight AI Coding Agent Persistent Memory Engine CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  recall save --title "Auth Decision" --content "Use JWT tokens for API auth" --category decision --tags auth,jwt
  recall search "authentication" --mode hybrid --limit 10
  recall show 42
  recall dashboard --agent claude-code
  recall context --agent cursor --max-tokens 2000
  recall session start --agent copilot --description "Refactoring auth module"
  recall export --format json --output memories.json
        """
    )
    parser.add_argument("-v", "--version", action="version",
                        version=f"AgentRecall v{__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # save command
    save_parser = subparsers.add_parser("save", help="💾 Save a new memory")
    save_parser.add_argument("--title", "-t", required=True, help="Memory title")
    save_parser.add_argument("--content", "-c", required=True, help="Memory content")
    save_parser.add_argument("--category", "-k", default="general",
                             help="Category (decision/bug/feature/context/architecture/lesson/config/workflow/general)")
    save_parser.add_argument("--tags", help="Comma-separated tags")
    save_parser.add_argument("--importance", "-i", type=float, default=0.5,
                             help="Importance score (0.0-1.0)")
    save_parser.add_argument("--agent", "-a", default="default", help="Agent ID")
    save_parser.add_argument("--session", "-s", default="", help="Session ID")

    # search command
    search_parser = subparsers.add_parser("search", help="🔍 Search memories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--mode", "-m", default="hybrid",
                               choices=["hybrid", "fulltext", "keyword", "tfidf"],
                               help="Search mode")
    search_parser.add_argument("--category", "-k", help="Filter by category")
    search_parser.add_argument("--limit", "-l", type=int, default=20, help="Max results")
    search_parser.add_argument("--agent", "-a", default="default", help="Agent ID")
    search_parser.add_argument("--min-importance", type=float, default=0.0,
                               help="Minimum importance threshold")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # show command
    show_parser = subparsers.add_parser("show", help="👁️ Show memory details")
    show_parser.add_argument("id", type=int, help="Memory ID")

    # list command
    list_parser = subparsers.add_parser("list", help="📋 List recent memories")
    list_parser.add_argument("--category", "-k", help="Filter by category")
    list_parser.add_argument("--limit", "-l", type=int, default=20, help="Max results")
    list_parser.add_argument("--agent", "-a", default="default", help="Agent ID")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="🗑️ Delete a memory")
    delete_parser.add_argument("id", type=int, help="Memory ID")
    delete_parser.add_argument("--force", "-f", action="store_true",
                               help="Skip confirmation")

    # update command
    update_parser = subparsers.add_parser("update", help="✏️ Update a memory")
    update_parser.add_argument("id", type=int, help="Memory ID")
    update_parser.add_argument("--title", "-t", help="New title")
    update_parser.add_argument("--content", "-c", help="New content")
    update_parser.add_argument("--category", "-k", help="New category")
    update_parser.add_argument("--tags", help="New comma-separated tags")
    update_parser.add_argument("--importance", "-i", type=float, help="New importance")

    # dashboard command
    dash_parser = subparsers.add_parser("dashboard", help="📊 Show dashboard")
    dash_parser.add_argument("--agent", "-a", default="default", help="Agent ID")

    # context command
    ctx_parser = subparsers.add_parser("context", help="📋 Generate agent context")
    ctx_parser.add_argument("--agent", "-a", default="default", help="Agent ID")
    ctx_parser.add_argument("--max-tokens", type=int, default=4000,
                            help="Max token budget for context")
    ctx_parser.add_argument("--categories", help="Comma-separated categories to include")
    ctx_parser.add_argument("--output", "-o", help="Output to file")

    # session commands
    session_parser = subparsers.add_parser("session", help="🔄 Session management")
    session_sub = session_parser.add_subparsers(dest="session_cmd")

    start_parser = session_sub.add_parser("start", help="Start a new session")
    start_parser.add_argument("--agent", "-a", default="default", help="Agent ID")
    start_parser.add_argument("--description", "-d", default="", help="Session description")

    end_parser = session_sub.add_parser("end", help="End current session")
    end_parser.add_argument("--summary", "-s", default="", help="Session summary")

    history_parser = session_sub.add_parser("history", help="Show session history")
    history_parser.add_argument("--agent", "-a", default="default", help="Agent ID")
    history_parser.add_argument("--limit", "-l", type=int, default=10)

    # export command
    export_parser = subparsers.add_parser("export", help="📤 Export memories")
    export_parser.add_argument("--format", "-f", default="json",
                               choices=["json", "markdown"], help="Export format")
    export_parser.add_argument("--output", "-o", help="Output file path")
    export_parser.add_argument("--agent", "-a", default="default", help="Agent ID")

    # import command
    import_parser = subparsers.add_parser("import", help="📥 Import memories")
    import_parser.add_argument("file", help="Input file path")
    import_parser.add_argument("--agent", "-a", default="default", help="Agent ID")
    import_parser.add_argument("--format", "-f", default="json",
                               choices=["json"], help="Import format")

    # stats command
    stats_parser = subparsers.add_parser("stats", help="📈 Show statistics")
    stats_parser.add_argument("--agent", "-a", default="default", help="Agent ID")
    stats_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # agents command
    subparsers.add_parser("agents", help="🤖 List registered agents")

    # categories command
    cat_parser = subparsers.add_parser("categories", help="📂 List categories")
    cat_parser.add_argument("--agent", "-a", default="default", help="Agent ID")

    # cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="🧹 Cleanup old memories")
    cleanup_parser.add_argument("--max-age-days", type=int, default=90,
                                help="Max age in days")
    cleanup_parser.add_argument("--min-importance", type=float, default=0.3,
                                help="Min importance to keep")
    cleanup_parser.add_argument("--agent", "-a", default="default", help="Agent ID")
    cleanup_parser.add_argument("--dry-run", action="store_true",
                                help="Show what would be deleted")

    # compress command
    compress_parser = subparsers.add_parser("compress", help="🗜️ Compress memory content")
    compress_parser.add_argument("id", type=int, help="Memory ID")
    compress_parser.add_argument("--apply", action="store_true",
                                 help="Apply compression to the memory")

    # suggest command
    suggest_parser = subparsers.add_parser("suggest", help="💡 Suggest related memories")
    suggest_parser.add_argument("id", type=int, help="Memory ID")
    suggest_parser.add_argument("--limit", "-l", type=int, default=5)

    return parser


def cmd_save(args, store: MemoryStore, compressor: MemoryCompressor):
    """Handle save command."""
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []

    # Auto-compress content if too long
    result = compressor.compress(args.content)
    content = result["compressed"]

    memory_id = store.save_memory(
        agent_id=args.agent,
        category=args.category,
        title=args.title,
        content=content,
        tags=tags,
        importance=args.importance,
        session_id=args.session
    )

    print(f"{Colors.GREEN}✅ Memory saved successfully!{Colors.RESET}")
    print(f"  {Colors.DIM}ID: #{memory_id}{Colors.RESET}")
    print(f"  {Colors.DIM}Category: {args.category}{Colors.RESET}")
    if tags:
        print(f"  {Colors.DIM}Tags: {', '.join(tags)}{Colors.RESET}")
    if result["ratio"] < 1.0:
        print(f"  {Colors.DIM}Compressed: {result['original_length']} → {result['compressed_length']} "
              f"({result['ratio']:.0%}){Colors.RESET}")


def cmd_search(args, store: MemoryStore, engine: SearchEngine, tui: TUIDashboard):
    """Handle search command."""
    results = engine.search(
        query=args.query,
        agent_id=args.agent,
        mode=args.mode,
        category=args.category,
        limit=args.limit,
        min_importance=args.min_importance
    )

    if args.json:
        # Remove internal fields for JSON output
        clean = []
        for r in results:
            clean.append({k: v for k, v in r.items() if not k.startswith("_")})
        print(json.dumps(clean, indent=2, ensure_ascii=False, default=str))
    else:
        tui.show_search_results(results, args.query)


def cmd_show(args, store: MemoryStore, tui: TUIDashboard):
    """Handle show command."""
    tui.show_memory_detail(args.id)


def cmd_list(args, store: MemoryStore, tui: TUIDashboard):
    """Handle list command."""
    memories = store.get_recent(args.agent, args.limit, args.category)

    if args.json:
        print(json.dumps(memories, indent=2, ensure_ascii=False, default=str))
    else:
        tui.show_search_results(memories)


def cmd_delete(args, store: MemoryStore):
    """Handle delete command."""
    if not args.force:
        mem = store.get_memory(args.id)
        if mem:
            print(f"{Colors.YELLOW}⚠️  Delete memory #{args.id}: {mem['title']}?{Colors.RESET}")
            confirm = input(f"  {Colors.DIM}Type 'yes' to confirm: {Colors.RESET}").strip().lower()
            if confirm != "yes":
                print(f"{Colors.DIM}Cancelled.{Colors.RESET}")
                return

    success = store.delete_memory(args.id)
    if success:
        print(f"{Colors.GREEN}🗑️  Memory #{args.id} deleted.{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Memory #{args.id} not found.{Colors.RESET}")


def cmd_update(args, store: MemoryStore):
    """Handle update command."""
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None

    success = store.update_memory(
        memory_id=args.id,
        title=args.title,
        content=args.content,
        tags=tags,
        importance=args.importance,
        category=args.category
    )

    if success:
        print(f"{Colors.GREEN}✏️  Memory #{args.id} updated.{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Memory #{args.id} not found.{Colors.RESET}")


def cmd_dashboard(args, store: MemoryStore, engine: SearchEngine, tui: TUIDashboard):
    """Handle dashboard command."""
    tui.show_dashboard(args.agent)


def cmd_context(args, store: MemoryStore, tui: TUIDashboard):
    """Handle context command."""
    categories = None
    if args.categories:
        categories = [c.strip() for c in args.categories.split(",")]

    context = store.get_context_for_agent(
        agent_id=args.agent,
        max_tokens=args.max_tokens,
        categories=categories
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(context)
        print(f"{Colors.GREEN}📋 Context written to {args.output}{Colors.RESET}")
    else:
        tui.show_context_preview(context, args.agent)


def cmd_session(args, store: MemoryStore, session_mgr: SessionManager, tui: TUIDashboard):
    """Handle session commands."""
    if args.session_cmd == "start":
        sid = session_mgr.start_session(args.agent, description=args.description)
        print(f"{Colors.GREEN}🔄 Session started: {sid}{Colors.RESET}")

    elif args.session_cmd == "end":
        session_mgr.end_session(args.summary)
        print(f"{Colors.GREEN}🔄 Session ended.{Colors.RESET}")
        if args.summary:
            print(f"  {Colors.DIM}Summary saved.{Colors.RESET}")

    elif args.session_cmd == "history":
        sessions = session_mgr.get_session_history(args.agent, args.limit)
        if not sessions:
            print(f"{Colors.YELLOW}No sessions found.{Colors.RESET}")
            return

        tui._print_header("Session History", f"Agent: {args.agent}")
        for s in sessions:
            duration = ""
            if s["duration"]:
                mins = int(s["duration"] / 60)
                if mins < 60:
                    duration = f"{mins}m"
                else:
                    hours = mins // 60
                    remain = mins % 60
                    duration = f"{hours}h {remain}m"

            print(f"  {Colors.CYAN}🆔 {s['id'][:30]}{Colors.RESET}")
            print(f"     {Colors.DIM}Started: {time.ctime(s['started_at'])}{Colors.RESET}")
            if duration:
                print(f"     {Colors.DIM}Duration: {duration}{Colors.RESET}")
            print(f"     {Colors.DIM}Memories: {s['memory_count']}{Colors.RESET}")
            print()

    else:
        print(f"{Colors.YELLOW}Use: recall session start|end|history{Colors.RESET}")


def cmd_export(args, store: MemoryStore, tui: TUIDashboard):
    """Handle export command."""
    content = store.export_memories(args.agent, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{Colors.GREEN}📤 Exported to {args.output}{Colors.RESET}")
    else:
        tui.show_export(content, args.format)


def cmd_import(args, store: MemoryStore):
    """Handle import command."""
    with open(args.file, "r", encoding="utf-8") as f:
        data = f.read()

    count = store.import_memories(args.agent, data, args.format)
    print(f"{Colors.GREEN}📥 Imported {count} memories.{Colors.RESET}")


def cmd_stats(args, store: MemoryStore, tui: TUIDashboard):
    """Handle stats command."""
    stats = store.get_stats(args.agent)

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        tui._print_header("Memory Statistics", f"Agent: {args.agent}")
        for key, value in stats.items():
            label = key.replace("_", " ").title()
            print(f"  {Colors.CYAN}{label}:{Colors.RESET}  {Colors.BOLD}{value}{Colors.RESET}")
        print()


def cmd_agents(store: MemoryStore, tui: TUIDashboard):
    """Handle agents command."""
    tui.show_agents()


def cmd_categories(args, store: MemoryStore, tui: TUIDashboard):
    """Handle categories command."""
    tui.show_categories(args.agent)


def cmd_cleanup(args, store: MemoryStore):
    """Handle cleanup command."""
    if args.dry_run:
        # Show what would be deleted
        cutoff = time.time() - (args.max_age_days * 86400)
        conn = store.conn
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM memories
            WHERE agent_id = ? AND created_at < ? AND importance < ?
        """, (args.agent, cutoff, args.min_importance))
        count = cursor.fetchone()["cnt"]
        print(f"{Colors.YELLOW}🧹 Dry run: would delete {count} memories "
              f"(older than {args.max_age_days} days, importance < {args.min_importance}){Colors.RESET}")
    else:
        deleted = store.cleanup_old_memories(args.agent, args.max_age_days, args.min_importance)
        print(f"{Colors.GREEN}🧹 Cleaned up {deleted} old memories.{Colors.RESET}")


def cmd_compress(args, store: MemoryStore, compressor: MemoryCompressor):
    """Handle compress command."""
    mem = store.get_memory(args.id)
    if not mem:
        print(f"{Colors.RED}❌ Memory #{args.id} not found.{Colors.RESET}")
        return

    result = compressor.compress(mem["content"])

    print(f"{Colors.CYAN}🗜️  Compression Result:{Colors.RESET}")
    print(f"  Original:   {result['original_length']} chars")
    print(f"  Compressed: {result['compressed_length']} chars")
    print(f"  Ratio:      {result['ratio']:.0%}")
    print(f"  Hash:       {result['hash']}")
    print()

    if args.apply:
        store.update_memory(args.id, content=result["compressed"])
        print(f"{Colors.GREEN}✅ Memory #{args.id} compressed and updated.{Colors.RESET}")
    else:
        print(f"{Colors.DIM}Preview (first 500 chars):{Colors.RESET}")
        print(f"{Colors.DIM}{result['compressed'][:500]}{Colors.RESET}")
        print()
        print(f"{Colors.DIM}Use --apply to update the memory.{Colors.RESET}")


def cmd_suggest(args, store: MemoryStore, engine: SearchEngine, tui: TUIDashboard):
    """Handle suggest command."""
    related = engine.suggest_related(args.id, args.limit)
    if related:
        tui._print_header("Related Memories", f"Memory #{args.id}")
        for r in related:
            score = r.get("_score", 0)
            print(f"  {Colors.DIM}#{r['id']}{Colors.RESET} "
                  f"{Colors.BOLD}{r['title'][:50]}{Colors.RESET} "
                  f"{Colors.GREEN}(score: {score:.2f}){Colors.RESET}")
        print()
    else:
        print(f"{Colors.YELLOW}No related memories found.{Colors.RESET}")


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize components
    store = MemoryStore()
    engine = SearchEngine(store)
    compressor = MemoryCompressor()
    session_mgr = SessionManager(store)
    tui = TUIDashboard(store, engine)

    try:
        if args.command == "save":
            cmd_save(args, store, compressor)
        elif args.command == "search":
            cmd_search(args, store, engine, tui)
        elif args.command == "show":
            cmd_show(args, store, tui)
        elif args.command == "list":
            cmd_list(args, store, tui)
        elif args.command == "delete":
            cmd_delete(args, store)
        elif args.command == "update":
            cmd_update(args, store)
        elif args.command == "dashboard":
            cmd_dashboard(args, store, engine, tui)
        elif args.command == "context":
            cmd_context(args, store, tui)
        elif args.command == "session":
            cmd_session(args, store, session_mgr, tui)
        elif args.command == "export":
            cmd_export(args, store, tui)
        elif args.command == "import":
            cmd_import(args, store)
        elif args.command == "stats":
            cmd_stats(args, store, tui)
        elif args.command == "agents":
            cmd_agents(store, tui)
        elif args.command == "categories":
            cmd_categories(args, store, tui)
        elif args.command == "cleanup":
            cmd_cleanup(args, store)
        elif args.command == "compress":
            cmd_compress(args, store, compressor)
        elif args.command == "suggest":
            cmd_suggest(args, store, engine, tui)
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print(f"\n{Colors.DIM}Interrupted.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)
    finally:
        store.close()


if __name__ == "__main__":
    main()
