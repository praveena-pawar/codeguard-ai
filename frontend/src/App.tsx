import { useState } from "react";
import Editor from "@monaco-editor/react";

const defaultCode = `def divide(a, b):
    return a / b
`;

type Issue = {
  rule: string;
  message: string;
  line: number;
  severity: string;
  explanation: string;
};

type TestResult = {
  passed: boolean;
  return_code: number;
  stdout: string;
  stderr: string;
};

type AnalysisResult = {
  issues: Issue[];
  before_score: number;
  after_score: number;
  tests: {
    code: string;
    original: TestResult;
    fixed: TestResult;
  };
  fix: {
    code: string;
    validated: boolean;
  };
};



function formatExplanation(text: string) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line, index) => {
      const cleaned = line
        .replace(/^\*\*\d+\.\*\*\s*/, "")
        .replace(/^\d+\.\s*/, "")
        .replace(/^\*\*\s*/, "")
        .replace(/^-+\s*/, "")
        .replace(/\*\*$/g, "");

      const parts = cleaned.split(/\*\*(.*?)\*\*/g);

      return (
        <p
          key={index}
          className="text-sm leading-6 text-slate-300"
        >
          {parts.map((part, partIndex) =>
            partIndex % 2 === 1 ? (
              <strong
                key={partIndex}
                className="font-semibold text-slate-100"
              >
                {part}
              </strong>
            ) : (
              part
            )
          )}
        </p>
      );
    });
}


function App() {
  const [code, setCode] = useState(defaultCode);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [error, setError] = useState("");

  const analyzeCode = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    setAnalysisStep(1);

    const stepTimer1 = setTimeout(() => {
      setAnalysisStep(2);
    }, 1500);

    const stepTimer2 = setTimeout(() => {
      setAnalysisStep(3);
    }, 3500);

    const stepTimer3 = setTimeout(() => {
      setAnalysisStep(4);
    }, 5500);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/analysis`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code }),
      });

      if (!response.ok) {
        throw new Error("Analysis request failed");
      }

      setAnalysisStep(5);

      const data: AnalysisResult = await response.json();

      setResult(data);
      setAnalysisStep(6);
    } catch (err) {
      console.error(err);

      setError(
        "CodeGuard could not complete the analysis. Check that the backend is running and try again."
      );
    } finally {
      clearTimeout(stepTimer1);
      clearTimeout(stepTimer2);
      clearTimeout(stepTimer3);

      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* HEADER */}
      <header className="border-b border-slate-800 px-8 py-5">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              CodeGuard <span className="text-cyan-400">AI</span>
            </h1>

            <p className="mt-1 text-sm text-slate-400">
              AI-powered code review, testing, and fixing
            </p>
          </div>

          <div className="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-400">
            Python
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-8 py-8">
        {/* TITLE */}
        <div className="mb-6">
          <h2 className="text-xl font-semibold">Analyze your code</h2>

          <p className="mt-1 text-sm text-slate-400">
            Find issues, generate tests, and validate AI-powered fixes.
          </p>
        </div>

        {/* TOP SECTION */}
        <div className="grid items-start gap-6 lg:grid-cols-2">

          {/* SOURCE CODE */}
          <section className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
            <div className="flex items-center justify-between border-b border-slate-800 px-5 py-3">
              <span className="text-sm font-medium">Source Code</span>

              <button
                className="rounded-lg bg-cyan-500 px-5 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
                onClick={analyzeCode}
                disabled={loading}
              >
                {loading ? "Analyzing..." : "Analyze Code"}
              </button>
            </div>

            <Editor
              height="500px"
              language="python"
              theme="vs-dark"
              value={code}
              onChange={(value) => setCode(value ?? "")}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                padding: { top: 16 },
                scrollBeyondLastLine: false,
              }}
            />
          </section>

          {/* ANALYSIS RESULTS */}
          <section className="space-y-4">

            {loading && (
              <div className="rounded-xl border border-cyan-900 bg-slate-900 p-6">
                <div className="flex items-center gap-3">
                  <div className="h-3 w-3 animate-pulse rounded-full bg-cyan-400" />

                  <h3 className="font-semibold text-slate-100">
                    CodeGuard is analyzing your code
                  </h3>
                </div>

                <div className="mt-5 space-y-3">
                  {[
                    "Static analysis",
                    "AI explanation",
                    "Test generation",
                    "Running tests",
                    "Generating fix",
                    "Validating fix",
                  ].map((step, index) => {
                    const stepNumber = index + 1;
                    const completed = analysisStep > stepNumber;
                    const active = analysisStep === stepNumber;

                    return (
                      <div
                        key={step}
                        className="flex items-center gap-3 text-sm"
                      >
                        <div
                          className={`flex h-6 w-6 items-center justify-center rounded-full border text-xs ${
                            completed
                              ? "border-green-800 text-green-400"
                              : active
                              ? "border-cyan-700 text-cyan-400"
                              : "border-slate-700 text-slate-600"
                          }`}
                        >
                          {completed ? "✓" : active ? "⟳" : "○"}
                        </div>

                        <span
                          className={
                            completed
                              ? "text-green-400"
                              : active
                              ? "text-cyan-400"
                              : "text-slate-600"
                          }
                        >
                          {step}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* QUALITY SCORE */}
            <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-slate-400">
                    Code Quality
                  </p>

                  <div className="mt-2 flex items-baseline gap-2">
                    <p className="text-5xl font-bold text-cyan-400">
                      {result ? result.after_score : "--"}
                    </p>

                    {result && (
                      <span className="text-sm text-slate-500">
                        / 100
                      </span>
                    )}
                  </div>
                </div>

                <div
                  className={`rounded-full border px-4 py-2 text-sm ${
                    result
                      ? "border-green-800 bg-green-950/30 text-green-400"
                      : "border-slate-700 text-slate-400"
                  }`}
                >
                  {result ? "✓ Analysis complete" : "Awaiting analysis"}
                </div>
              </div>

              {result && (
                <>
                  {/* SCORE PROGRESS */}
                  <div className="mt-6">
                    <div className="flex items-center justify-between text-xs text-slate-500">
                      <span>Quality improvement</span>
                      <span>{result.after_score}%</span>
                    </div>

                    <div className="mt-2 h-3 overflow-hidden rounded-full bg-slate-800">
                      <div
                        className="h-full rounded-full bg-cyan-400 transition-all duration-1000"
                        style={{
                          width: `${result.after_score}%`,
                        }}
                      />
                    </div>
                  </div>

                  {/* BEFORE / IMPROVEMENT / AFTER */}
                  <div className="mt-6 grid grid-cols-3 gap-3">
                    <div className="rounded-lg border border-slate-800 bg-slate-950/50 p-4">
                      <p className="text-xs uppercase tracking-wide text-slate-500">
                        Before
                      </p>

                      <p className="mt-2 text-2xl font-bold text-slate-300">
                        {result.before_score}
                      </p>

                      <p className="mt-1 text-xs text-slate-500">
                        Initial quality
                      </p>
                    </div>

                    <div className="flex flex-col items-center justify-center rounded-lg border border-green-900 bg-green-950/20 p-4 text-center">
                      <p className="text-xs uppercase tracking-wide text-slate-500">
                        Improvement
                      </p>

                      <p className="mt-2 text-2xl font-bold text-green-400">
                        +{result.after_score - result.before_score}
                      </p>

                      <p className="mt-1 text-xs text-green-400">
                        Quality gained
                      </p>
                    </div>

                    <div className="rounded-lg border border-cyan-900 bg-cyan-950/20 p-4">
                      <p className="text-xs uppercase tracking-wide text-slate-500">
                        After
                      </p>

                      <p className="mt-2 text-2xl font-bold text-cyan-400">
                        {result.after_score}
                      </p>

                      <p
                        className={`mt-1 text-xs ${
                          result.fix.validated
                            ? "text-green-400"
                            : "text-red-400"
                        }`}
                      >
                        {result.fix.validated
                          ? "Fix validated"
                          : "Fix needs review"}
                      </p>
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* DETECTED ISSUES */}
            <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="font-semibold">Detected Issues</h3>

              {!result && !error && (
                <div className="mt-5 rounded-lg border border-dashed border-slate-700 p-6 text-center">
                  <p className="text-sm text-slate-500">
                    Run an analysis to see detected issues.
                  </p>
                </div>
              )}

              {result && result.issues.length === 0 && (
                <div className="mt-5 rounded-lg border border-slate-700 p-5">
                  <p className="text-sm text-green-400">
                    No issues detected.
                  </p>
                </div>
              )}

              {result && result.issues.length > 0 && (
                <div className="mt-5 space-y-3">
                  {result.issues.map((issue, index) => (
                    <div
                      key={index}
                      className="rounded-lg border border-slate-700 p-4"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-cyan-400">
                          {issue.rule}
                        </span>

                        <span className="text-xs uppercase text-amber-400">
                          {issue.severity}
                        </span>
                      </div>

                      <p className="mt-2 text-sm text-slate-300">
                        {issue.message}
                      </p>

                      <p className="mt-2 text-xs text-slate-500">
                        Line {issue.line}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>
        </div>

        {/* AI EXPLANATION — FULL WIDTH */}
        <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h3 className="font-semibold">AI Explanation</h3>

          {!result && (
            <p className="mt-4 text-sm leading-6 text-slate-500">
              CodeGuard will explain what went wrong, why it matters, and
              how to fix it.
            </p>
          )}

          {result && result.issues.length > 0 && (
            <div className="mt-4 space-y-5">
              {result.issues.map((issue, index) => (
                <div
                  key={index}
                  className="rounded-lg border border-slate-800 bg-slate-950/50 p-4"
                >
                  <div className="mb-3 flex items-center justify-between">
                    <span className="text-sm font-semibold text-cyan-400">
                      {issue.rule}
                    </span>

                    <span className="text-xs text-slate-500">
                      Line {issue.line}
                    </span>
                  </div>

                  <div className="max-h-32 overflow-y-auto pr-2 space-y-2">
                    {formatExplanation(issue.explanation)}
                  </div>
                </div>
              ))}
            </div>
          )}

          {error && (
            <div className="mt-4 rounded-lg border border-red-900 bg-red-950/40 p-5">
              <div className="flex items-center gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-full border border-red-800 text-red-400">
                  !
                </div>

                <div>
                  <p className="font-semibold text-red-400">
                    Analysis failed
                  </p>

                  <p className="mt-1 text-sm text-red-300/80">
                    {error}
                  </p>
                </div>
              </div>

              <button
                onClick={analyzeCode}
                className="mt-4 rounded-lg border border-red-800 px-4 py-2 text-sm font-medium text-red-400 transition hover:bg-red-950"
              >
                Try Again
              </button>
            </div>
          )}
        </div>

        {/* BEFORE + AFTER CODE */}
        {result && (
          <section className="mt-6 overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
            <div className="border-b border-slate-800 px-5 py-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold">Code Improvement</h3>
                  <p className="mt-1 text-sm text-slate-500">
                    Compare the original code with the AI-generated fix.
                  </p>
                </div>

                <span
                  className={`rounded-full border px-3 py-1 text-xs font-medium ${
                    result.fix.validated
                      ? "border-green-800 text-green-400"
                      : "border-red-800 text-red-400"
                  }`}
                >
                  {result.fix.validated
                    ? "✓ Fix Verified"
                    : "✗ Fix Needs Review"}
                </span>
              </div>
            </div>

            <div className="grid lg:grid-cols-2">
              {/* BEFORE */}
              <div className="border-b border-slate-800 lg:border-b-0 lg:border-r">
                <div className="flex items-center justify-between border-b border-slate-800 px-5 py-3">
                  <span className="text-sm font-medium">Before</span>

                  <span className="text-xs text-red-400">
                    {result.issues.length} issue
                    {result.issues.length !== 1 ? "s" : ""} detected
                  </span>
                </div>

                <Editor
                  height="320px"
                  language="python"
                  theme="vs-dark"
                  value={code}
                  options={{
                    readOnly: true,
                    minimap: { enabled: false },
                    fontSize: 13,
                    padding: { top: 16 },
                    scrollBeyondLastLine: false,
                  }}
                />
              </div>

              {/* AFTER */}
              <div>
                <div className="flex items-center justify-between border-b border-slate-800 px-5 py-3">
                  <span className="text-sm font-medium">After</span>

                  <span className="text-xs text-green-400">
                    {result.fix.validated
                      ? "Validated fix"
                      : "Validation failed"}
                  </span>
                </div>

                <Editor
                  height="320px"
                  language="python"
                  theme="vs-dark"
                  value={result.fix.code}
                  options={{
                    readOnly: true,
                    minimap: { enabled: false },
                    fontSize: 13,
                    padding: { top: 16 },
                    scrollBeyondLastLine: false,
                  }}
                />
              </div>
            </div>
          </section>
        )}

        {/* TESTS + FIX */}
        {result && (
          <div className="mt-6 grid gap-6 lg:grid-cols-2">

            {/* GENERATED TESTS */}
            <section className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
              <div className="flex items-center justify-between border-b border-slate-800 px-5 py-4">
                <h3 className="font-semibold">Generated Tests</h3>

                <span
                  className={`rounded-full px-3 py-1 text-xs font-medium ${
                    result.tests.original.passed
                      ? "border border-green-800 text-green-400"
                      : "border border-red-400 text-red-400"
                  }`}
                >
                  {result.tests.original.passed
                    ? "✓ Original Passed"
                    : "✗ Original Failed"}
                </span>
              </div>

              <Editor
                height="350px"
                language="python"
                theme="vs-dark"
                value={result.tests.code}
                options={{
                  readOnly: true,
                  minimap: { enabled: false },
                  fontSize: 13,
                  padding: { top: 16 },
                  scrollBeyondLastLine: false,
                }}
              />

              <div className="border-t border-slate-800">
                <div className="grid grid-cols-2">
                  <div className="border-r border-slate-800 p-5">
                    <p className="text-xs uppercase tracking-wide text-slate-500">
                      Original Code
                    </p>

                    <p
                      className={`mt-2 text-sm font-semibold ${
                        result.tests.original.passed
                          ? "text-green-400"
                          : "text-red-400"
                      }`}
                    >
                      {result.tests.original.passed
                        ? "✓ Tests Passed"
                        : "✗ Tests Failed"}
                    </p>
                  </div>

                  <div className="p-5">
                    <p className="text-xs uppercase tracking-wide text-slate-500">
                      Fixed Code
                    </p>

                    <p
                      className={`mt-2 text-sm font-semibold ${
                        result.tests.fixed.passed
                          ? "text-green-400"
                          : "text-red-400"
                      }`}
                    >
                      {result.tests.fixed.passed
                        ? "✓ Tests Passed"
                        : "✗ Tests Failed"}
                    </p>
                  </div>
                </div>

                {/* TEST OUTPUT */}
                <div className="border-t border-slate-800 p-5">
                  <details>
                    <summary className="cursor-pointer text-sm font-medium text-slate-300 hover:text-cyan-400">
                      View original test output
                    </summary>

                    <pre className="mt-4 max-h-64 overflow-auto rounded-lg border border-slate-800 bg-slate-950 p-4 text-xs leading-5 text-slate-400">
                      {result.tests.original.stdout ||
                        result.tests.original.stderr ||
                        "No test output available."}
                    </pre>
                  </details>

                  <details className="mt-3">
                    <summary className="cursor-pointer text-sm font-medium text-slate-300 hover:text-green-400">
                      View fixed test output
                    </summary>

                    <pre className="mt-4 max-h-64 overflow-auto rounded-lg border border-slate-800 bg-slate-950 p-4 text-xs leading-5 text-slate-400">
                      {result.tests.fixed.stdout ||
                        result.tests.fixed.stderr ||
                        "No test output available."}
                    </pre>
                  </details>
                </div>
              </div>
            </section>

            {/* AI FIX */}
            <section className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
              <div className="flex items-center justify-between border-b border-slate-800 px-5 py-4">
                <h3 className="font-semibold">AI Fix</h3>

                <span
                  className={`rounded-full px-3 py-1 text-xs font-medium ${
                    result.fix.validated
                      ? "border border-green-800 text-green-400"
                      : "border border-red-800 text-red-400"
                  }`}
                >
                  {result.fix.validated
                    ? "✓ Fix Validated"
                    : "✗ Validation Failed"}
                </span>
              </div>

              <Editor
                height="350px"
                language="python"
                theme="vs-dark"
                value={result.fix.code}
                options={{
                  readOnly: true,
                  minimap: { enabled: false },
                  fontSize: 13,
                  padding: { top: 16 },
                  scrollBeyondLastLine: false,
                }}
              />

              <div className="border-t border-slate-800 px-5 py-4">
                <p className="text-sm text-slate-400">
                  Test result after fix:
                </p>

                <p
                  className={`mt-1 text-sm font-medium ${
                    result.tests.fixed.passed
                      ? "text-green-400"
                      : "text-red-400"
                  }`}
                >
                  {result.tests.fixed.passed
                    ? "✓ All generated tests passed"
                    : "✗ Generated tests failed"}
                </p>
              </div>
            </section>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;