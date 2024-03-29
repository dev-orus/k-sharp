import { join, dirname } from "path";
const parentDir = dirname(dirname(__dirname));

import {
  createConnection,
  TextDocuments,
  Diagnostic,
  DiagnosticSeverity,
  ProposedFeatures,
  InitializeParams,
  DidChangeConfigurationNotification,
  CompletionItem,
  CompletionItemKind,
  TextDocumentPositionParams,
  TextDocumentSyncKind,
  InitializeResult,
  DocumentDiagnosticReportKind,
  type DocumentDiagnosticReport,
  CompletionParams,
  ConnectionStrategy,
  FoldingRangeRequest,
} from "vscode-languageserver/node";
import { TextDocument } from "vscode-languageserver-textdocument";
import { existsSync } from "fs";
import { ChildProcessWithoutNullStreams, execSync, spawn } from "child_process";
import { platform } from "os";
import { dir } from "console";

// TODO: Make a way to open a workspace folder and check if the currently open file has a string that starts with a directory on workspaceFodlers
function readPY(): Promise<{ [key: string]: any }> {
  return new Promise((resolve) => {
    let stderrOutput = "";

    pySockets[currentWorkspace].stderr.on("data", (chunk) => {
      stderrOutput += chunk.toString();
      try {
        resolve(JSON.parse(stderrOutput));
      } catch (e) {}
    });
  });
}
const IS_WINDOWS = platform() == "win32";
const envType = IS_WINDOWS ? "Scripts" : "bin";
const lspData: { env: string; file: string } = {
  env: join(parentDir, 'env', envType, 'python3'),
  file: join(parentDir, 'lsp.py')
}
// const lspData: { env: string; file: string } = JSON.parse(
  // execSync(IS_WINDOWS ? "powershell wisp-lsp" : "bash wisp-lsp").toString()
// );
const connection = createConnection(ProposedFeatures.all);
const documents: TextDocuments<TextDocument> = new TextDocuments(TextDocument);
var workspaceFolders: string[] = [];
var currentWorkspace: string = "{global}";
var pySockets: { [key: string]: ChildProcessWithoutNullStreams } = {
  "{global}": spawn(lspData.env, [lspData.file], {
    stdio: ["pipe", "pipe", "pipe"],
  }),
};

function useWorkspaceFolder(wf: string) {
  const envPath = join(wf.replace(/^file:/, ""), ".env", envType, "python3");
  if (existsSync(envPath)) {
    if (!Object.keys(pySockets).includes(wf)) {
      pySockets[wf] = spawn(envPath, [lspData.file], {
        stdio: ["pipe", "pipe", "pipe"],
      });
    }
    currentWorkspace = wf;
  } else {
    currentWorkspace = "{global}";
  }
}

function checkWorkspace(filePath: string) {
  workspaceFolders
    .sort((a, b) => b.length - a.length)
    .forEach((i) => {
      if (filePath.startsWith(i)) {
        useWorkspaceFolder(i);
      }
    });
}

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
  pySockets[currentWorkspace].stdin.write(JSON.stringify(toData) + "\n");
  let pyData = await readPY();
  let items: CompletionItem[] = [];
  Object.keys(pyData).forEach((i) => {
    if (pyData[i]["type"] == "statement")
      items.push({
        label: i,
        kind: CompletionItemKind.Variable,
        sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
        documentation: {
          kind: "markdown",
          value:
            "```wisp\n" +
            pyData[i].sign +
            "\n```\n" +
            pyData[i].doc,
        },
      });
    else if (pyData[i]["type"] == "keyword")
      items.push({
        label: i,
        kind: CompletionItemKind.Keyword,
        sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
        documentation: {
          kind: "markdown",
          value:
            "```wisp\n" +
            pyData[i].sign +
            "\n```\n" +
            pyData[i].doc,
        },
      });
    else if (pyData[i]["type"] == "class")
      items.push({
        label: i,
        kind: CompletionItemKind.Class,
        sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
        documentation: {
          kind: "markdown",
          value:
            "```wisp\n" +
            pyData[i].sign +
            "\n```\n" +
            pyData[i].doc,
        },
      });
    else if (pyData[i]["type"] == "function")
      items.push({
        label: i,
        kind: CompletionItemKind.Function,
        sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
        documentation: {
          kind: "markdown",
          value:
            "```wisp\n" +
            pyData[i].sign +
            "\n```\n" +
            pyData[i].doc,
        },
      });
    else if (pyData[i]["type"] == "module")
      items.push({
        label: i,
        kind: CompletionItemKind.Module,
        insertText: i + (pyData[i]["glb"] ? ">" : ""),
        sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
        documentation: {
          kind: "markdown",
          value:
            "```wisp\n" +
            pyData[i].sign +
            "\n```\n" +
            pyData[i].doc,
        },
      });
    else if (pyData[i]["type"] == "method")
      items.push({
        label: i,
        kind: CompletionItemKind.Method,
        sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
        documentation: {
          kind: "markdown",
          value:
            "```wisp\n" +
            pyData[i].sign +
            "\n```\n" +
            pyData[i].doc,
        },
      });
    else if (pyData[i]["type"] == "instance")
      items.push({
        label: i,
        kind: CompletionItemKind.Variable,
        sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
        documentation: {
          kind: "markdown",
          value:
            "```wisp\n" +
            pyData[i].sign +
            "\n```\n" +
            pyData[i].doc
        },
      });
    else if (pyData[i]["type"] == "param")
      items.push({
        label: i,
        kind: CompletionItemKind.Property,
        sortText: i.startsWith("__") ? "c" : i.startsWith("_") ? "b" : "a",
        documentation: {
          kind: "markdown",
          value:
            "```wisp\n" +
            pyData[i].sign +
            "\n```\n" +
            pyData[i].doc,
        },
      });
    else {
    }
  });
  return items;
});

connection.onExit(() => {
  Object.keys(pySockets).forEach((i) => {
    pySockets[i].kill();
  });
});

connection.onInitialize((params): InitializeResult => {
  if (params.workspaceFolders) {
    params.workspaceFolders.forEach((workspaceFolder) => {
      workspaceFolders.push(workspaceFolder.uri);
    });
  }
  return {
    capabilities: {
      textDocumentSync: TextDocumentSyncKind.Incremental,
      definitionProvider: true,
      completionProvider: {
        triggerCharacters: ["#", ".", ":", "<", ">", '"'],
      },
    },
  };
});

documents.listen(connection);
connection.listen();
  