import csv
import sys
import traci

SEED = sys.argv[1] if len(sys.argv) > 1 else "1"
APPROACHES = ["N_in", "S_in", "E_in", "W_in"]

traci.start(["sumo", "-n", "junction.net.xml", "-r", "demand.rou.xml",
             "--seed", SEED])

rows = []
arrived = 0
step = 0

while traci.simulation.getMinExpectedNumber() > 0 and step < 3600:
    traci.simulationStep()
    arrived += traci.simulation.getArrivedNumber()
    step += 1

    vehicles = traci.vehicle.getIDList()
    waits = [traci.vehicle.getWaitingTime(v) for v in vehicles]
    avg_wait = sum(waits) / len(waits) if waits else 0.0
    queue = sum(traci.edge.getLastStepHaltingNumber(e) for e in APPROACHES)
    phase = traci.trafficlight.getPhase("C")

    rows.append([step, phase, len(vehicles), round(avg_wait, 2), queue])

traci.close()

with open(f"metrics_fixed_{SEED}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["step", "phase", "vehicles", "avg_wait_s", "queue"])
    w.writerows(rows)

print("done:", step, "steps, seed", SEED, "arrived:", arrived)