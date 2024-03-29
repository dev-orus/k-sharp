"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const path_1 = require("path");
const parentDir = (0, path_1.dirname)((0, path_1.dirname)(__dirname));
const node_1 = require("vscode-languageserver/node");
const vscode_languageserver_textdocument_1 = require("vscode-languageserver-textdocument");
const fs_1 = require("fs");
const child_process_1 = require("child_process");
const os_1 = require("os");
// TODO: Make a way to open a workspace folder and check if the currently open file has a string that starts with a directory on workspaceFodlers
function readPY() {
    return new Promise((resolve) => {
        let stderrOutput = "";
        pySockets[currentWorkspace].stderr.on("data", (chunk) => {
            stderrOutput += chunk.toString();
            console.log(stderrOutput);
            try {
                resolve(JSON.parse(stderrOutput));
            }
            catch (e) { }
        });
    });
}
const IS_WINDOWS = (0, os_1.platform)() == "win32";
const envType = IS_WINDOWS ? "Scripts" : "bin";
const lspData = {
    env: (0, path_1.join)(parentDir, 'env', envType, 'python3'),
    file: (0, path_1.join)(parentDir, 'lsp.py')
};
// const lspData: { env: string; file: string } = JSON.parse(
// execSync(IS_WINDOWS ? "powershell wisp-lsp" : "bash wisp-lsp").toString()
// );
const connection = (0, node_1.createConnection)(node_1.ProposedFeatures.all);
const documents = new node_1.TextDocuments(vscode_languageserver_textdocument_1.TextDocument);
var workspaceFolders = [];
var currentWorkspace = "{global}";
var pySockets = {
    "{global}": (0, child_process_1.spawn)(lspData.env, [lspData.file], {
        stdio: ["pipe", "pipe", "pipe"],
    }),
};
function useWorkspaceFolder(wf) {
    const envPath = (0, path_1.join)(wf.replace(/^file:/, ""), ".env", envType, "python3");
    if ((0, fs_1.existsSync)(envPath)) {
        if (!Object.keys(pySockets).includes(wf)) {
            pySockets[wf] = (0, child_process_1.spawn)(envPath, [lspData.file], {
                stdio: ["pipe", "pipe", "pipe"],
            });
        }
        currentWorkspace = wf;
    }
    else {
        currentWorkspace = "{global}";
    }
}
function checkWorkspace(filePath) {
    workspaceFolders
        .sort((a, b) => b.length - a.length)
        .forEach((i) => {
        if (filePath.startsWith(i)) {
            useWorkspaceFolder(i);
        }
    });
}
console.log(".");
connection.onDefinition(async ({ textDocument, position }) => {
    let document = documents.get(textDocument.uri);
    if (!document) {
        return null;
    }
    checkWorkspace(textDocument.uri);
    let toData = {
        type: "definition",
        source: document.getText(),
        file: document.uri.replace(/^file:/, ""),
        line: position.line + 1,
        col: position.character,
    };
    pySockets[currentWorkspace].stdin.write(JSON.stringify(toData) + "\n");
    let pyData = await readPY();
    return [
        {
            uri: `file:${pyData.file}`,
            range: {
                start: { line: pyData.line - 1, character: pyData.col },
                end: { line: pyData.line - 1, character: pyData.col },
            },
        },
    ];
});
connection.onCompletion(async (params) => {
    console.log('Hello, World!');
    let document = documents.get(params.textDocument.uri);
    if (!document) {
        return null;
    }
    checkWorkspace(params.textDocument.uri);
    let toData = {
        type: "completion",
        source: document.getText(),
        file: document.uri.replace(/^file:/, ""),
        line: params.position.line + 1,
        col: params.position.character,
    };
    console.log(pySockets, currentWorkspace, JSON.stringify(toData));
    pySockets[currentWorkspace].stdin.write(JSON.stringify(toData) + "\n");
    let pyData = await readPY();
    let items = [];
    Object.keys(pyData).forEach((i) => {
        if (pyData[i]["type"] == "statement")
            items.push({
                label: i,
                kind: node_1.CompletionItemKind.Variable,
                sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
                documentation: {
                    kind: "markdown",
                    value: "```wisp\n" +
                        pyData[i].sign +
                        "\n```\n" +
                        pyData[i].doc,
                },
            });
        else if (pyData[i]["type"] == "keyword")
            items.push({
                label: i,
                kind: node_1.CompletionItemKind.Keyword,
                sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
                documentation: {
                    kind: "markdown",
                    value: "```wisp\n" +
                        pyData[i].sign +
                        "\n```\n" +
                        pyData[i].doc,
                },
            });
        else if (pyData[i]["type"] == "class")
            items.push({
                label: i,
                kind: node_1.CompletionItemKind.Class,
                sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
                documentation: {
                    kind: "markdown",
                    value: "```wisp\n" +
                        pyData[i].sign +
                        "\n```\n" +
                        pyData[i].doc,
                },
            });
        else if (pyData[i]["type"] == "function")
            items.push({
                label: i,
                kind: node_1.CompletionItemKind.Function,
                sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
                documentation: {
                    kind: "markdown",
                    value: "```wisp\n" +
                        pyData[i].sign +
                        "\n```\n" +
                        pyData[i].doc,
                },
            });
        else if (pyData[i]["type"] == "module")
            items.push({
                label: i,
                kind: node_1.CompletionItemKind.Module,
                insertText: i + (pyData[i]["glb"] ? ">" : ""),
                sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
                documentation: {
                    kind: "markdown",
                    value: "```wisp\n" +
                        pyData[i].sign +
                        "\n```\n" +
                        pyData[i].doc,
                },
            });
        else if (pyData[i]["type"] == "method")
            items.push({
                label: i,
                kind: node_1.CompletionItemKind.Method,
                sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
                documentation: {
                    kind: "markdown",
                    value: "```wisp\n" +
                        pyData[i].sign +
                        "\n```\n" +
                        pyData[i].doc,
                },
            });
        else if (pyData[i]["type"] == "instance")
            items.push({
                label: i,
                kind: node_1.CompletionItemKind.Variable,
                sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
                documentation: {
                    kind: "markdown",
                    value: "```wisp\n" +
                        pyData[i].sign +
                        "\n```\n" +
                        pyData[i].doc
                },
            });
        else if (pyData[i]["type"] == "param")
            items.push({
                label: i,
                kind: node_1.CompletionItemKind.Property,
                sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
                documentation: {
                    kind: "markdown",
                    value: "```wisp\n" +
                        pyData[i].sign +
                        "\n```\n" +
                        pyData[i].doc,
                },
            });
        else {
            console.log([i, pyData[i]]);
        }
    });
    return items;
});
connection.onExit(() => {
    Object.keys(pySockets).forEach((i) => {
        pySockets[i].kill();
    });
});
connection.onInitialize((params) => {
    if (params.workspaceFolders) {
        params.workspaceFolders.forEach((workspaceFolder) => {
            workspaceFolders.push(workspaceFolder.uri);
        });
    }
    return {
        capabilities: {
            textDocumentSync: node_1.TextDocumentSyncKind.Incremental,
            definitionProvider: true,
            completionProvider: {
                triggerCharacters: ["#", ".", ":", "<", ">", '"'],
            },
        },
    };
});
documents.listen(connection);
connection.listen();
//# sourceMappingURL=index.js.map