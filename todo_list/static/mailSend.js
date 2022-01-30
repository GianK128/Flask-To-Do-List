const sendBtn = document.getElementById('sendBtn');
let tmpCountDown = 0;
let tmpCountDownInterval;

sendBtn.addEventListener('click', (e) => {
    sendBtn.textContent = 'Enviando...';
    fetch('./verify/send-email')
    .then(response => {
        if (response.status === 200) {
            sendBtn.disabled = true;
            sendBtn.classList.add('btn-disabled');
            sendBtn.textContent = 'Reenviar correo (00:30)'
            startCountDown(30, 1000);
        }
    });
});

const countDown = () => {
    tmpCountDown -= 1;

    sendBtn.textContent = `Reenviar correo (00:${tmpCountDown.toString().padStart(2, '0')})`

    if (tmpCountDown <= 0) {
        stopCountDown();
    }
}

const startCountDown = (startingValue, timePeriod) => {
    tmpCountDown = startingValue;
    tmpCountDownInterval = setInterval(countDown, timePeriod);
}
const stopCountDown = () => {
    sendBtn.disabled = false;
    sendBtn.classList.remove('btn-disabled');
    sendBtn.textContent = 'Reenviar correo';
    clearInterval(tmpCountDownInterval);
}
