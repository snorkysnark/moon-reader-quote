export { EpubCFI } from "epubjs";

const WHITESPACE_REGEX = RegExp(/^[\n\s]*$/);

export class TaggedText {
    nodePositions: Map<number, Node>;
    plainText: string;

    constructor(root?: Node) {
        let plainText = "";
        let nodePositions = new Map<number, Node>();
        let isFirst = true;
        let lastWasWhitespace = false;

        let walker = document.createTreeWalker(
            root || document.body,
            NodeFilter.SHOW_TEXT
        );

        while (walker.nextNode()) {
            let node = walker.currentNode;
            if (!node.textContent) continue;

            if (WHITESPACE_REGEX.test(node.textContent)) {
                if (!lastWasWhitespace) {
                    lastWasWhitespace = true;

                    if (!isFirst) {
                        // Don't put a separator at the beginning
                        plainText += " ";
                    }
                }
            } else {
                lastWasWhitespace = false;
                nodePositions.set(plainText.length, node);
                plainText += node.textContent;
            }
            isFirst = false;
        }
        if (lastWasWhitespace) {
            // Remove a separator from the end
            plainText = plainText.slice(0, -1);
        }

        this.plainText = plainText;
        this.nodePositions = nodePositions;
    }

    findPosition(desiredOffset: number): [Node, number] {
        const positonIter = this.nodePositions.entries();
        let [lastOffset, lastNode] = (() => {
            const firstEntry = positonIter.next();
            if (firstEntry.done) {
                throw "Node map is empty";
            }

            return firstEntry.value as [number, Node];
        })();

        for (const [currentOffset, currentNode] of positonIter) {
            if (desiredOffset < currentOffset) break;

            lastOffset = currentOffset;
            lastNode = currentNode;
        }

        return [lastNode, desiredOffset - lastOffset];
    }

    construcRange(fromOffset: number, toOffset: number) {
        const [nodeFrom, nodeFromOffset] = this.findPosition(fromOffset);
        const [nodeTo, nodeToOffset] = this.findPosition(toOffset);

        let range = document.createRange();
        range.setStart(nodeFrom, nodeFromOffset);
        range.setEnd(nodeTo, nodeToOffset);

        return range;
    }
}

export function selectRange(range: Range, target_window?: Window) {
    target_window = target_window || window;

    let sel = target_window.getSelection()!;
    sel?.removeAllRanges();
    sel.addRange(range);
}
