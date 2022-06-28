import path from "path";
import { defineConfig } from "vite";

export default defineConfig({
    build: {
        lib: {
            entry: path.resolve(__dirname, "src/lib.ts"),
            name: "MoonQuote",
            formats: ["es"],
            fileName: (format) => `moon-quote.${format}.js`,
        },
    },
});
