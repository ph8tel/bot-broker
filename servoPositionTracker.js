let currentPositions = [
    1500,
    1500,
    1500,
    1500
]

const servoTracker = (movement, servo) => {
    movement = Number(movement)
    //  console.log('moving, current pos1', currentPositions[0], ' servo2: ', currentPositions[1] , ' servo to move: ', servo, ' amount: ', movement)
    let adjustedPostion;


    if ((movement + currentPositions[servo]) > 2000) {
        adjustedPostion = 2000;
    } else if ((movement + currentPositions[servo]) < 1000) {
        adjustedPostion = 1000;
    } else {
        adjustedPostion = movement += currentPositions[servo]
    }
    currentPositions[servo] = adjustedPostion
    return adjustedPostion;

};

for (let i = 0; i > -20; i -= 1) {
    console.log(servoTracker(-100, 0))
}
console.log('yo', servoTracker('-100', 0))