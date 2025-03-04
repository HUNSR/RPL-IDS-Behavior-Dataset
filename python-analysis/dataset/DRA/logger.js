const totalNodes = sim.getMotes().length; // Get the total number of nodes in the simulation
const minNodes = 2; // Minimum node ID
const maxNodes = totalNodes; // Maximum node ID

log.log(`Simulation has ${totalNodes} nodes. Setting maxNodes to ${maxNodes}.\n`);

const total_attacks = totalNodes;
const simulationDuration = 36000; // Total simulation time in seconds (20 hours)
TIMEOUT(36000000); // * 1000 to convert sec to millisecond

// Attack constructor
function Attack(name, targetID, startTime, duration) {
    this.name = name;
    this.t = sim.getMoteWithID(targetID);
    this.st = startTime * 1000000; // start time in microsecond
    this.et = this.st + (duration * 1000000); // Duration in microsecond
    this.ON = false;
    this.OFF = false;

    this.memAccess = function (varName, ithByte, byteValue) {
        mem = this.t.getMemory();
        exists = mem.getSymbolMap().containsKey(varName);
        if (exists) {
            sym = mem.getSymbolMap().get(varName);
            mem_seg = mem.getMemorySegment(sym.addr, sym.size);
            mem_seg[ithByte] = byteValue;
            mem.setMemorySegment(sym.addr, mem_seg);
            return true;
        }
        return false;
    };

    this.flipSwitch = function (time) {
        if (!this.ON && time > this.st) {
            this.ON = this.memAccess(this.name, 0, 0xff);
            if (this.ON) log.log(time + " " + this.t.getID() + " ibs: " + this.name + " ON\n");
        }
        if (!this.OFF && time > this.et) {
            this.OFF = this.memAccess(this.name, 0, 0x00);
            if (this.OFF) log.log(time + " " + this.t.getID() + " ibs: " + this.name + " OFF\n");
        }
    };
}

// Initialize attack names
// const attackNames = ["VNA_on", "DRA_on", "DISA_on" , "SFA_on"];
const attackNames = [ "DRA_on"];
const minDuration = 5000; // Minimum duration in seconds (10 minutes)
const maxDuration = 10000; // Maximum duration in seconds (20 minutes)

attacks = [];

// Function to check if the new attack time conflicts with existing attacks on the same node
function isTimeConflict(targetNode, startTime, endTime) {
    const margin = 1000000 * 120;
    startTime = startTime - margin;
    endTime = endTime + margin;

    for (let i = 0; i < attacks.length; i++) {
        const existingAttack = attacks[i];
        if (existingAttack.t.getID() === targetNode) {
            // Check if there is an overlap in time
            if (
                (startTime >= existingAttack.st && startTime < existingAttack.et) ||
                (endTime > existingAttack.st && endTime <= existingAttack.et) ||
                (startTime <= existingAttack.st && endTime >= existingAttack.et)
            ) {
                return true; // Conflict found
            }
        }
    }
    return false; // No conflict
}

// Function to create and add a random attack
function addRandomAttack() {
    const attackType = attackNames[Math.floor(Math.random() * attackNames.length)];
    const targetNode = Math.floor(Math.random() * (maxNodes - minNodes + 1)) + minNodes;
    const startTime = Math.floor(Math.random() * (simulationDuration - minDuration)); // Random start time within the hour
    const duration = Math.floor(Math.random() * (maxDuration - minDuration)) + minDuration;

    const endTime = startTime * 1000000 + duration * 1000000;

    // Retry if there's a time conflict for this node
    if (!isTimeConflict(targetNode, startTime * 1000000, endTime)) {
        const newAttack = new Attack(attackType, targetNode, startTime, duration);
        attacks.push(newAttack);
    } else {
        // Recursively attempt to add a new non-conflicting attack
        addRandomAttack();
    }
}

// Create a random attack every few minutes
for (let i = 0; i < total_attacks; i++) {
    addRandomAttack();
}

// Log the content of the attacks array
log.log(`Attacks array contents length: ${attacks.length} \n`);
for (let i = 0; i < attacks.length; i++) {
    log.log(`Attack Name: ${attacks[i].name}, Target ID: ${attacks[i].t.getID()}, Start Time: ${attacks[i].st}, End Time: ${attacks[i].et}\n`);
}

log.log("Starting COOJA logger with random attacks\n");

timeout_function = function () {
    log.log("Script timed out.\n");
    log.testOK();
};

// Main simulation loop
while (true) {
    if (msg) {
        log.log(time + " " + id + " " + msg + "\n");
    }
    for (i = 0; i < attacks.length; i++) {
        attacks[i].flipSwitch(time);
    }
    YIELD();
}
