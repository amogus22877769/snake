let offset;
let iteration = 1;

onmessage = (e) => {
  offset = e.data;
  setTimeout(loop, offset + 100 - performance.now());
};

function loop() {
  postMessage(performance.now() - (offset + iteration * 100));
  iteration += 1;
  setTimeout(loop, offset + iteration * 100 - performance.now());
}
