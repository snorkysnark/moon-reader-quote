import "./style.css";
import { TaggedText, EpubCFI, selectRange } from "./lib.js";

let iframe = document.getElementById("book-frame")! as HTMLIFrameElement;

new ResizeObserver((entries) => {
    let height = entries[0].target.scrollHeight;
    iframe.style.height = height + 50 + "px";
}).observe(iframe.contentDocument!.body);

iframe.addEventListener("load", () => {
    let framedoc = iframe.contentDocument!;
    let framewin = iframe.contentWindow!;

    (window as any).framewin = framewin;
    (window as any).taggedtext = new TaggedText(framedoc.body);
    (window as any).selectRange = (range: Range) => selectRange(range, framewin);
    (window as any).epubCfi = EpubCFI;
});
