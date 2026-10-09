import csv
import sys
import traci

SEED = sys.argv[1] if len(sys.argv) > 1 else "1"
TLS = "C"
MIN_GREEN, MAX_GREEN, YELLOW = 15, 60, 3
NS = ["N_in", "S_in"]
EW = ["E_in", "W_in"]
APPROACHES = NS + EW

# green phase index -> (own arms, crossing arms, yellow phase index)
GREEN = {0: (NS, EW, 1), 3: (EW, NS, 4)}


def queue(arms):
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


traci.start(["sumo", "-n", "junction.net.xml", "-r", "demand.rou.xml",
             "--seed", SEED])

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
        if should_switch(elapsed, queue(own), queue(cross)):
            traci.trafficlight.setPhase(TLS, yellow)
            traci.trafficlight.setPhaseDuration(TLS, YELLOW)

    vehicles = traci.vehicle.getIDList()
    waits = [traci.vehicle.getWaitingTime(v) for v in vehicles]
    avg_wait = sum(waits) / len(waits) if waits else 0.0
    rows.append([step, phase, len(vehicles), round(avg_wait, 2), queue(APPROACHES)])

traci.close()

with open(f"metrics_adaptive_{SEED}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["step", "phase", "vehicles", "avg_wait_s", "queue"])
    w.writerows(rows)

print("done:", step, "steps, seed", SEED, "arrived:", arrived)