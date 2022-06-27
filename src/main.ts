import "./style.css";
import TaggedText from "./lib.js";

let iframe = document.getElementById("book-frame")! as HTMLIFrameElement;

new ResizeObserver((entries) => {
    let height = entries[0].target.scrollHeight;
    iframe.style.height = height + 50 + "px";
}).observe(iframe.contentDocument!.body);

iframe.addEventListener("load", () => {
    let framedoc = iframe.contentDocument!;

    (window as any).framewin = iframe.contentWindow!;
    (window as any).taggedtext = new TaggedText(framedoc.body);
});
