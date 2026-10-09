import bisect
import csv
import json
import sys
import traci

SEED = sys.argv[1] if len(sys.argv) > 1 else "1"
DELAY_MS = sys.argv[2] if len(sys.argv) > 2 else "100"
USE_CV = (sys.argv[3] if len(sys.argv) > 3 else "sim") == "cv"

TLS = "C"
MIN_GREEN, MAX_GREEN, YELLOW = 15, 60, 3
NS = ["N_in", "S_in"]
EW = ["E_in", "W_in"]
APPROACHES = NS + EW

# green phase index -> (own arms, crossing arms, yellow phase index)
GREEN = {0: (NS, EW, 1), 3: (EW, NS, 4)}

# ---- CV counts (only used when argv[3] == "cv") ----
CV_SCALE = 1.0
LOOP_CV = True
CV_RECORDS = []
if USE_CV:
    with open("outputs/lane_counts.jsonl") as f:
        CV_RECORDS = [json.loads(line) for line in f if line.strip()]
CV_TIMES = [r["t"] for r in CV_RECORDS]
CLIP_LEN = (CV_TIMES[-1] + 5.0) if CV_TIMES else 0.0


def cv_approaches(sim_t):
    t = sim_t % CLIP_LEN if (LOOP_CV and CLIP_LEN) else sim_t
    i = bisect.bisect_right(CV_TIMES, t) - 1
    return CV_RECORDS[max(i, 0)]["approaches"]


def queue(arms, step):
    if USE_CV:
        counts = cv_approaches(step)
        return CV_SCALE * sum(counts[a] for a in arms)
    return sum(traci.edge.getLastStepHaltingNumber(e) for e in arms)

def should_switch(elapsed, own_q, cross_q):
    # always end at max green
    if elapsed >= MAX_GREEN:
        return True
    # hold at least the minimum green
    if elapsed < MIN_GREEN:
        return False
    # gap-out: current direction is clear and the other side is waiting
    return own_q == 0 and cross_q > 0


traci.start(["sumo-gui", "-n", "junction.net.xml", "-r", "demand.rou.xml",
             "-g", "gui.settings.xml",
             "--seed", SEED, "--delay", DELAY_MS, "--start"])

rows = []
step = 0
arrived = 0
last_phase = None
phase_start = 0

while traci.simulation.getMinExpectedNumber() > 0 and step < 600:
    traci.simulationStep()
    step += 1
    arrived += traci.simulation.getArrivedNumber()

    phase = traci.trafficlight.getPhase(TLS)
    if phase != last_phase:
        last_phase = phase
        phase_start = step
        if phase in GREEN:
            traci.trafficlight.setPhaseDuration(TLS, MAX_GREEN)

    if phase in GREEN:
        own, cross, yellow = GREEN[phase]
        elapsed = step - phase_start
        if should_switch(elapsed, queue(own, step), queue(cross, step)):
            traci.trafficlight.setPhase(TLS, yellow)
            traci.trafficlight.setPhaseDuration(TLS, YELLOW)

    vehicles = traci.vehicle.getIDList()
    waits = [traci.vehicle.getWaitingTime(v) for v in vehicles]
    avg_wait = sum(waits) / len(waits) if waits else 0.0
    rows.append([step, phase, len(vehicles), round(avg_wait, 2),
                 queue(APPROACHES, step)])

traci.close()

with open(f"metrics_adaptive_gui_{SEED}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["step", "phase", "vehicles", "avg_wait_s", "queue"])
    w.writerows(rows)

print("done:", step, "steps, seed", SEED, "arrived:", arrived)