import handleWASD from "./handleWASD";
import { socket } from "./socket";

export default function unMountGameHandlers(): void {
  socket.off("new_snake");
  socket.off("new_apple");
  socket.off("change_direction");
  document.removeEventListener("keydown", handleWASD);
}
