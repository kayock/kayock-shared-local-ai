"""Command-line interface for Kayock AI Resource Governor."""

from __future__ import annotations

import argparse
import json
import sys

from governor import __version__
from governor.benchmark import run_benchmark, save_benchmark
from governor.handoff import describe_lifecycle, observe_handoff
from governor.lemonade import check_lemonade
from governor.optimizer import Optimizer
from governor.persistence import init_db
from governor.profiles import PROFILES, WorkloadProfile
from governor.telemetry import collect_telemetry, format_metric, telemetry_to_dict


def cmd_status(args: argparse.Namespace) -> int:
    snapshot = collect_telemetry()
    lemonade = check_lemonade()
    handoff = observe_handoff(telemetry=snapshot)

    if args.json:
        payload = {
            "telemetry": telemetry_to_dict(snapshot),
            "lemonade": {
                "online": lemonade.online,
                "authenticated": lemonade.authenticated,
                "health_status": lemonade.health_status,
                "model_loaded": lemonade.model_loaded,
                "models": lemonade.models,
                "error": lemonade.error,
            },
            "handoff": {
                "state": handoff.state.value,
                "vram_used_mib": handoff.vram_used_mib,
                "vram_free_mib": handoff.vram_free_mib,
                "notes": handoff.notes,
            },
        }
        print(json.dumps(payload, indent=2))
        return 0

    gpu = snapshot.gpu
    print("KAYOCK AI RESOURCE GOVERNOR — STATUS")
    print("=" * 40)
    print("GPU")
    print(f"  Name:         {format_metric(gpu.name)}")
    print(f"  Utilization:  {format_metric(gpu.utilization_percent)} %")
    print(f"  VRAM used:    {format_metric(gpu.vram_used_mib)} MiB")
    print(f"  VRAM free:    {format_metric(gpu.vram_free_mib)} MiB")
    print(f"  Temperature:  {format_metric(gpu.temperature_c)} °C")
    print(f"  Clock:        {format_metric(gpu.clock_graphics_mhz)} MHz")
    print(f"  Power draw:   {format_metric(gpu.power_draw_w)} W")
    print(f"  Power limit:  {format_metric(gpu.power_limit_w)} W")
    print(f"  Throttle:     {format_metric(gpu.throttle_reasons)}")
    print()
    print("SYSTEM")
    print(f"  CPU:          {format_metric(snapshot.system.cpu_percent)} %")
    print(f"  RAM:          {format_metric(snapshot.system.ram_used_mib)} / "
          f"{format_metric(snapshot.system.ram_total_mib)} MiB "
          f"({format_metric(snapshot.system.ram_percent)} %)")
    print()
    print("LEMONADE")
    print(f"  Online:       {lemonade.online}")
    print(f"  Auth:         {lemonade.authenticated}")
    if lemonade.health_status:
        print(f"  Health:       {lemonade.health_status}")
    print(f"  Model:        {lemonade.model_loaded or 'unknown'}")
    if lemonade.error:
        print(f"  Error:        {lemonade.error}")
    print()
    print("HANDOFF")
    print(f"  State:        {handoff.state.value}")
    for note in handoff.notes:
        print(f"  Note:         {note}")
    return 0


def cmd_benchmark(args: argparse.Namespace) -> int:
    init_db()
    profile = args.profile or "default"
    run = run_benchmark(profile_name=profile)
    path = save_benchmark(run)

    if args.json:
        from dataclasses import asdict
        print(json.dumps(asdict(run), indent=2))
    else:
        print(f"Benchmark run: {run.run_id}")
        print(f"  Profile:  {run.profile_name}")
        print(f"  Model:    {run.model}")
        print(f"  TTFT avg: {run.aggregate_ttft_s}")
        print(f"  TPS avg:  {run.aggregate_tps}")
        print(f"  Errors:   {len(run.errors)}")
        if run.errors:
            for e in run.errors:
                print(f"    - {e}")
        print(f"  Saved:    {path}")

    return 1 if run.errors else 0


def cmd_optimize(args: argparse.Namespace) -> int:
    init_db()
    workload = WorkloadProfile(args.profile)
    opt = Optimizer(workload)
    if args.baseline_only:
        run = opt.record_baseline()
        print(f"Baseline recorded: score context in DB, run {run.run_id}")
        return 1 if run.errors else 0

    result = opt.optimize()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Optimization complete: {result['workload']}")
        print(f"  Baseline score: {result['baseline_score']}")
        print(f"  Best score:     {result['best_score']}")
        print(f"  Active config:  {result['active_config']}")
        for c in result.get("candidates", []):
            print(f"  {c['decision']}: {c['candidate']} — {c['reason']}")
    return 0


def cmd_profiles(args: argparse.Namespace) -> int:
    data = {k.value: v.to_dict() for k, v in PROFILES.items()}
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        for name, prof in data.items():
            print(f"{name}: {prof['description']}")
            print(f"  request: {prof['request']}")
            print(f"  prioritize: {prof['prioritize']}")
    return 0


def cmd_handoff(args: argparse.Namespace) -> int:
    if args.lifecycle:
        for step in describe_lifecycle():
            print(f"{step['state']}: {step['description']}")
        return 0
    obs = observe_handoff()
    if args.json:
        print(json.dumps({
            "state": obs.state.value,
            "vram_used_mib": obs.vram_used_mib,
            "vram_free_mib": obs.vram_free_mib,
            "lemonade_model": obs.lemonade_model,
            "lemonade_online": obs.lemonade_online,
            "notes": obs.notes,
        }, indent=2))
    else:
        print(f"Handoff state: {obs.state.value}")
        print(f"VRAM free: {obs.vram_free_mib} MiB")
        for n in obs.notes:
            print(f"  {n}")
    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    from governor.dashboard import run_dashboard
    run_dashboard()
    return 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="governor",
        description="Kayock AI Resource Governor v0.1",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", help="Show telemetry and Lemonade status")
    p_status.add_argument("--json", action="store_true")
    p_status.set_defaults(func=cmd_status)

    p_bench = sub.add_parser("benchmark", help="Run Lemonade benchmark harness")
    p_bench.add_argument("--profile", default="default")
    p_bench.add_argument("--json", action="store_true")
    p_bench.set_defaults(func=cmd_benchmark)

    p_opt = sub.add_parser("optimize", help="Run safe configuration optimizer")
    p_opt.add_argument(
        "--profile",
        default="LOW_LATENCY",
        choices=[p.value for p in WorkloadProfile],
    )
    p_opt.add_argument("--baseline-only", action="store_true")
    p_opt.add_argument("--json", action="store_true")
    p_opt.set_defaults(func=cmd_optimize)

    p_prof = sub.add_parser("profiles", help="List workload profiles")
    p_prof.add_argument("--json", action="store_true")
    p_prof.set_defaults(func=cmd_profiles)

    p_hand = sub.add_parser("handoff", help="Observe GPU handoff state")
    p_hand.add_argument("--json", action="store_true")
    p_hand.add_argument("--lifecycle", action="store_true")
    p_hand.set_defaults(func=cmd_handoff)

    p_dash = sub.add_parser("dashboard", help="Start local web dashboard")
    p_dash.set_defaults(func=cmd_dashboard)

    args = parser.parse_args(argv)
    sys.exit(args.func(args))
