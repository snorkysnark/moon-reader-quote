class TaggedText {
    nodePositions: Map<number, Node>;
    plainText: string;

    constructor(root?: Node) {
        let plainText = "";
        let nodePositions = new Map<number, Node>();

        let walker = document.createTreeWalker(
            root || document.body,
            NodeFilter.SHOW_TEXT
        );

        while (walker.nextNode()) {
            let node = walker.currentNode;
            if (!node.textContent) continue;

            nodePositions.set(plainText.length, node);
            plainText += node.textContent;
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

export default TaggedText;
