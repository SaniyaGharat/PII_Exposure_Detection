import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  AlertCircle,
  ArrowLeft,
  ArrowRight,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Clipboard,
  CloudUpload,
  Copy,
  FileText,
  Fingerprint,
  LoaderCircle,
  LockKeyhole,
  RotateCw,
  Settings2,
  ShieldCheck,
  Sparkles,
  X,
  XCircle,
} from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Switch } from "@/components/ui/switch";
import {
  analyzeDocument,
  anchorDocument,
  countFields,
  domains,
  getSamples,
  overrideField,
  sampleTexts,
  verifyDocument,
  visibleFields,
  type AnalyzeResult,
  type ApiSettings,
  type AuditField,
  type AuditStatus,
  type AnchorResult,
  type Domain,
  type SampleDocument,
  type VerifyResult,
} from "@/lib/pii-audit";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "PII Necessity Audit | Privacy Research Demo" },
      { name: "description", content: "A guided research demo for auditing personal information necessity and recording privacy-preserving decisions on-chain." },
      { property: "og:title", content: "PII Necessity Audit | Privacy Research Demo" },
      { property: "og:description", content: "Explore a four-step PII necessity audit: detect, review, anchor hashes, and verify the record." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: AuditPage,
});

const stepLabels = ["Select document", "Review findings", "Anchor on-chain", "Verify record"];
const initialDomain: Domain = "job_application";

function AuditPage() {
  const [step, setStep] = useState(1);
  const [unlockedStep, setUnlockedStep] = useState(1);
  const [domain, setDomain] = useState<Domain>(initialDomain);
  const [purpose, setPurpose] = useState(`${initialDomain}_review_and_processing`);
  const [documentText, setDocumentText] = useState(sampleTexts[initialDomain]);
  const [sampleId, setSampleId] = useState("sample-job-01");
  const [samples, setSamples] = useState<SampleDocument[]>([]);
  const [settings, setSettings] = useState<ApiSettings>({ baseUrl: "http://localhost:8000", mockMode: false });
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [hideLowSignal, setHideLowSignal] = useState(true);
  const [analysis, setAnalysis] = useState<AnalyzeResult | null>(null);
  const [anchor, setAnchor] = useState<AnchorResult | null>(null);
  const [verification, setVerification] = useState<VerifyResult | null>(null);
  const [selectedValue, setSelectedValue] = useState<string | null>(null);
  const [busyAction, setBusyAction] = useState<"samples" | "analyze" | "anchor" | "verify" | "override" | null>(null);
  const [error, setError] = useState<{ action: "samples" | "analyze" | "anchor" | "verify"; message: string } | null>(null);
  const [overrideFieldType, setOverrideFieldType] = useState<string | null>(null);
  const [overrideJustification, setOverrideJustification] = useState("");
  const [overriddenTypes, setOverriddenTypes] = useState<Set<string>>(() => new Set());
  const fileInputRef = useRef<HTMLInputElement>(null);
  const documentRef = useRef<HTMLPreElement>(null);

  useEffect(() => {
    let active = true;
    setBusyAction("samples");
    getSamples(settings)
      .then((result) => {
        if (active) {
          setSamples(result);
          const currentSample = result.find((s) => s.id === sampleId) || result[0];
          if (currentSample?.text) {
            setDocumentText(currentSample.text);
          }
        }
      })
      .catch((reason: unknown) => {
        if (active) setError({ action: "samples", message: messageFor(reason) });
      })
      .finally(() => { if (active) setBusyAction((current) => current === "samples" ? null : current); });
    return () => { active = false; };
  }, [settings]);

  const counts = useMemo(() => analysis ? countFields(analysis.fields) : null, [analysis]);
  const shownFields = useMemo(
    () => analysis ? visibleFields(analysis.fields, hideLowSignal) : [],
    [analysis, hideLowSignal],
  );
  const hiddenCount = analysis ? analysis.fields.length - shownFields.length : 0;

  function changeDomain(next: Domain) {
    setDomain(next);
    setPurpose(`${next}_review_and_processing`);
    const matchingSample = samples.find((sample) => sample.domain === next);
    setDocumentText(matchingSample?.text ?? sampleTexts[next]);
    setSampleId(matchingSample?.id ?? "uploaded");
    setAnalysis(null);
    setAnchor(null);
    setVerification(null);
    setOverriddenTypes(new Set());
    setUnlockedStep(1);
  }

  function chooseSample(id: string) {
    setSampleId(id);
    const selected = samples.find((sample) => sample.id === id);
    if (selected) {
      changeDomain(selected.domain);
      if (selected.text) {
        setDocumentText(selected.text);
      }
    }
  }

  async function runAnalyze() {
    setBusyAction("analyze"); setError(null); setAnalysis(null); setAnchor(null); setVerification(null);
    try {
      const result = await analyzeDocument(settings, { document_text: documentText, domain, purpose });
      setAnalysis(result); setStep(2); setUnlockedStep(2); setSelectedValue(null);
    } catch (reason) {
      setError({ action: "analyze", message: messageFor(reason) });
    } finally { setBusyAction(null); }
  }

  async function runAnchor() {
    if (!analysis) return;
    setBusyAction("anchor"); setError(null); setAnchor(null); setVerification(null);
    try {
      const result = await anchorDocument(settings, analysis.document_id);
      setAnchor(result); setStep(3); setUnlockedStep(4);
    } catch (reason) { setError({ action: "anchor", message: messageFor(reason) }); }
    finally { setBusyAction(null); }
  }

  async function runVerify() {
    if (!analysis || !anchor) return;
    setBusyAction("verify"); setError(null); setVerification(null);
    try {
      const result = await verifyDocument(settings, analysis.document_id);
      setVerification(result); setStep(4);
    } catch (reason) { setError({ action: "verify", message: messageFor(reason) }); }
    finally { setBusyAction(null); }
  }

  async function submitOverride() {
    if (!analysis || !overrideFieldType || overrideJustification.trim().length < 8) return;
    setBusyAction("override"); setError(null);
    try {
      const result = await overrideField(settings, {
        document_id: analysis.document_id,
        field_type: overrideFieldType,
        justification: overrideJustification.trim(),
      });
      setOverriddenTypes((previous) => new Set(previous).add(overrideFieldType));
      toast.success("Override recorded", { description: `Transaction ${shortHash(result.transaction_hash)}` });
      setOverrideFieldType(null); setOverrideJustification("");
    } catch (reason) { setError({ action: "analyze", message: messageFor(reason) }); }
    finally { setBusyAction(null); }
  }

  async function retry(action: "samples" | "analyze" | "anchor" | "verify") {
    if (action === "samples") {
      setError(null); setBusyAction("samples");
      try { setSamples(await getSamples(settings)); }
      catch (reason) { setError({ action, message: messageFor(reason) }); }
      finally { setBusyAction(null); }
    } else if (action === "analyze") await runAnalyze();
    else if (action === "anchor") await runAnchor();
    else await runVerify();
  }

  function highlightValue(value: string) {
    setSelectedValue(value);
    window.requestAnimationFrame(() => {
      const target = documentRef.current;
      if (!target) return;
      const text = target.textContent ?? "";
      const index = text.toLowerCase().indexOf(value.toLowerCase());
      if (index < 0) return;
      const before = target.textContent?.slice(0, index) ?? "";
      const linesAbove = before.split("\n").length - 1;
      target.scrollTop = Math.max(0, linesAbove * 29 - 96);
    });
  }

  function handleFile(file: File | undefined) {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".txt")) {
      toast.error("Please choose a .txt document");
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      setDocumentText(String(reader.result ?? "")); setSampleId("uploaded"); setAnalysis(null); setAnchor(null); setVerification(null); setUnlockedStep(1);
    };
    reader.onerror = () => toast.error("This document could not be read. Please try another .txt file.");
    reader.readAsText(file);
  }

  const compareRows = verification && analysis ? [
    { label: "Purpose", report: analysis.purpose, chain: verification.purpose, match: analysis.purpose === verification.purpose },
    { label: "Flagged fields", report: String(analysis.flagged_count), chain: String(verification.flagged_count), match: analysis.flagged_count === verification.flagged_count },
    { label: "Total fields", report: String(analysis.total_fields), chain: String(verification.total_field_count), match: analysis.total_fields === verification.total_field_count },
  ] : [];
  const recordMatches = compareRows.every((row) => row.match);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b border-border bg-card">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 py-4 sm:px-8">
          <div className="flex min-w-0 items-center gap-3">
            <div className="flex size-10 shrink-0 items-center justify-center rounded-md bg-primary text-primary-foreground"><Fingerprint className="size-5" /></div>
            <div className="min-w-0">
              <div className="truncate text-lg font-bold leading-tight">PII Necessity Audit</div>
              <p className="hidden text-sm text-muted-foreground sm:block">Privacy research prototype</p>
            </div>
          </div>
          <Button variant="outline" size="sm" onClick={() => setSettingsOpen(true)} aria-label="Open settings"><Settings2 className="size-4" /><span className="hidden sm:inline">Settings</span></Button>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-5 pb-12 pt-8 sm:px-8 sm:pt-10">
        <div className="mb-8 flex flex-col gap-2 sm:mb-10 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.14em] text-accent"><Sparkles className="size-4" /> Research demonstration</p>
            <h1 className="text-3xl font-bold leading-tight sm:text-4xl">Make data collection accountable.</h1>
            <p className="mt-2 max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg">Review what a document collects, question what it needs, and verify a privacy-preserving audit.</p>
          </div>
          <div className="flex w-fit items-center gap-2 rounded-md border border-border bg-card px-3 py-2 text-sm font-medium"><span className={`size-2.5 rounded-full ${settings.mockMode ? "bg-amber-500" : "bg-emerald-500 animate-pulse"}`} />{settings.mockMode ? "Mock Mode" : `Connected API (${settings.baseUrl})`}</div>
        </div>

        <nav aria-label="Audit steps" className="mb-9 overflow-x-auto border-y border-border bg-card">
          <ol className="grid min-w-[680px] grid-cols-4">
            {stepLabels.map((label, index) => {
              const number = index + 1;
              const active = step === number;
              const complete = number < step || (number === 2 && !!analysis && step > 2) || (number === 3 && !!anchor && step === 4);
              return (
                <li key={label}>
                  <button type="button" disabled={number > unlockedStep} onClick={() => setStep(number)} className={`flex min-h-[76px] w-full items-center gap-3 border-b-[3px] px-4 text-left transition-colors disabled:cursor-not-allowed disabled:opacity-45 sm:px-6 ${active ? "border-accent bg-accent/5" : complete ? "border-transparent" : "border-transparent"}`}>
                    <span className={`flex size-9 shrink-0 items-center justify-center rounded-full border text-sm font-bold ${active ? "border-accent bg-accent text-accent-foreground" : complete ? "border-accent bg-accent/10 text-accent" : "border-border bg-muted text-muted-foreground"}`}>{complete ? <Check className="size-4" /> : `0${number}`}</span>
                    <span className={`text-sm font-semibold sm:text-base ${active ? "text-foreground" : "text-muted-foreground"}`}>{label}</span>
                  </button>
                </li>
              );
            })}
          </ol>
        </nav>

        <section className="min-h-[580px]" aria-live="polite">
          {step === 1 && <section className="grid gap-8 lg:grid-cols-[0.88fr_1.12fr]">
            <div className="space-y-6">
              <div className="mb-1 flex items-start gap-4"><span className="flex size-12 shrink-0 items-center justify-center rounded-md bg-primary/8 text-primary"><FileText className="size-6" /></span><div><p className="mb-1 text-sm font-semibold text-accent">STEP 01</p><h2 className="text-2xl font-bold">Choose a document</h2><p className="mt-1 text-muted-foreground">Select a sample or bring your own text file.</p></div></div>
              <div className="space-y-2"><Label htmlFor="sample-select">Sample document</Label><div className="relative"><select id="sample-select" value={sampleId === "uploaded" ? "uploaded" : sampleId} onChange={(event) => chooseSample(event.target.value)} className="h-12 w-full appearance-none rounded-md border border-input bg-card px-3 pr-10 text-base focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"><option value="uploaded" disabled>Your uploaded document</option>{samples.map((sample) => <option key={sample.id} value={sample.id}>{sample.label}</option>)}</select><ChevronDown className="pointer-events-none absolute right-3 top-4 size-4 text-muted-foreground" /></div><p className="text-sm text-muted-foreground">{busyAction === "samples" ? "Loading sample documents…" : "Sample text stays in this browser when using demo mode."}</p></div>
              <div className="space-y-2"><Label htmlFor="domain-select">Document domain</Label><div className="relative"><select id="domain-select" value={domain} onChange={(event) => changeDomain(event.target.value as Domain)} className="h-12 w-full appearance-none rounded-md border border-input bg-card px-3 pr-10 text-base focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">{domains.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}</select><ChevronDown className="pointer-events-none absolute right-3 top-4 size-4 text-muted-foreground" /></div></div>
              <div className="space-y-2"><Label htmlFor="purpose">Audit purpose</Label><Input id="purpose" value={purpose} onChange={(event) => setPurpose(event.target.value)} className="h-12 text-base" /></div>
              <div className="flex flex-wrap gap-3 pt-1"><Button type="button" variant="outline" size="lg" onClick={() => fileInputRef.current?.click()}><CloudUpload className="size-5" />Upload .txt</Button><input ref={fileInputRef} type="file" accept=".txt,text/plain" className="hidden" onChange={(event) => handleFile(event.target.files?.[0])} /><Button type="button" size="lg" disabled={!documentText.trim() || busyAction === "analyze"} onClick={runAnalyze}>{busyAction === "analyze" ? <LoaderCircle className="size-5 animate-spin" /> : <ShieldCheck className="size-5" />}{busyAction === "analyze" ? "Analyzing…" : "Analyze document"}<ArrowRight className="size-4" /></Button></div>
              {error?.action === "samples" && <ErrorPanel error={error.message} onRetry={() => retry("samples")} />}
              {error?.action === "analyze" && <ErrorPanel error={error.message} onRetry={() => retry("analyze")} />}
            </div>
            <DocumentPreview documentText={documentText} selectedValue={selectedValue} documentRef={documentRef} />
          </section>}

          {step === 2 && analysis && counts && <div className="space-y-7">
            <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><p className="mb-1 text-sm font-semibold text-accent">STEP 02</p><h2 className="text-2xl font-bold sm:text-3xl">Detection &amp; necessity</h2><p className="mt-1 text-base text-muted-foreground">{domains.find((item) => item.id === analysis.domain)?.label} · {analysis.purpose}</p></div><div className="flex items-center gap-3 rounded-md border border-border bg-card px-4 py-3"><Switch id="low-signal" checked={hideLowSignal} onCheckedChange={setHideLowSignal} /><Label htmlFor="low-signal" className="cursor-pointer text-sm font-medium">Hide low-signal organization / URL detections</Label></div></div>
            <div className="grid grid-cols-2 gap-px overflow-hidden border border-border bg-border sm:grid-cols-4">
              <SummaryCard label="Total detected" number={analysis.total_fields} icon={<Fingerprint className="size-5" />} tone="neutral" />
              <SummaryCard label="Flagged" number={analysis.flagged_count} icon={<XCircle className="size-5" />} tone="flagged" />
              <SummaryCard label="Needs review" number={counts.review} icon={<AlertCircle className="size-5" />} tone="review" />
              <SummaryCard label="Cleared" number={counts.cleared} icon={<CheckCircle2 className="size-5" />} tone="cleared" />
            </div>
            {hiddenCount > 0 && hideLowSignal && <p className="flex items-start gap-2 rounded-md border border-accent/20 bg-accent/5 px-4 py-3 text-sm leading-relaxed text-accent"><AlertCircle className="mt-0.5 size-4 shrink-0" /><span>{hiddenCount} low-signal detection{hiddenCount === 1 ? "" : "s"} hidden (documented detector limitation); still included in the saved report.</span></p>}
            {error?.action === "analyze" && <ErrorPanel error={error.message} onRetry={() => retry("analyze")} />}
            <div className="overflow-hidden border border-border bg-card">
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border px-5 py-4"><div><h3 className="text-lg font-bold">Detected personal information</h3><p className="text-sm text-muted-foreground">Click a detected value to locate it in the source text.</p></div><span className="text-sm font-medium text-muted-foreground">Showing {shownFields.length} of {analysis.total_fields}</span></div>
              <div className="max-h-[680px] overflow-auto">
                <table className="w-full min-w-[850px] border-collapse text-left text-sm"><thead className="sticky top-0 z-10 bg-muted text-xs uppercase tracking-wide text-muted-foreground"><tr><th className="px-4 py-3 font-semibold">Field type</th><th className="px-4 py-3 font-semibold">Detected value</th><th className="w-40 px-4 py-3 font-semibold">Necessity N</th><th className="px-4 py-3 font-semibold">Status</th><th className="px-4 py-3 font-semibold">Action</th></tr></thead><tbody>
                  {shownFields.map((field, index) => <FieldRow key={`${field.field_type}-${index}`} field={field} selected={selectedValue === field.value} overridden={overriddenTypes.has(field.field_type)} onSelect={() => highlightValue(field.value)} onOverride={() => { setOverrideFieldType(field.field_type); setOverrideJustification(""); }} />)}
                  {shownFields.length === 0 && <tr><td colSpan={5} className="px-4 py-12 text-center text-muted-foreground">No visible detections. Turn on low-signal detections to view the full report.</td></tr>}
                </tbody></table>
              </div>
            </div>
            <DocumentPreview documentText={documentText} selectedValue={selectedValue} documentRef={documentRef} compact />
            <div className="flex flex-wrap justify-between gap-3"><Button variant="outline" size="lg" onClick={() => setStep(1)}><ArrowLeft className="size-4" />Back to document</Button><Button size="lg" disabled={busyAction === "anchor"} onClick={runAnchor}>{busyAction === "anchor" ? <LoaderCircle className="size-5 animate-spin" /> : <Fingerprint className="size-5" />}{busyAction === "anchor" ? "Anchoring…" : "Continue to blockchain"}<ArrowRight className="size-4" /></Button></div>
          </div>}

          {step === 3 && anchor && analysis && <div className="mx-auto max-w-4xl space-y-7">
            <div className="flex items-start gap-4"><span className="flex size-12 shrink-0 items-center justify-center rounded-md bg-accent/10 text-accent"><Fingerprint className="size-6" /></span><div><p className="mb-1 text-sm font-semibold text-accent">STEP 03</p><h2 className="text-2xl font-bold sm:text-3xl">Anchored on-chain</h2><p className="mt-1 text-base text-muted-foreground">The audit report is recorded on the local test blockchain.</p></div></div>
            <div className="grid gap-px overflow-hidden border border-border bg-border sm:grid-cols-2"><CopyValue label="Transaction hash" value={anchor.transaction_hash} mono /><CopyValue label="Block number" value={String(anchor.block_number)} mono={false} /><CopyValue label="Gas used" value={String(anchor.gas_used)} mono={false} /><CopyValue label="Document hash" value={anchor.doc_hash} mono /><CopyValue label="Report hash" value={anchor.report_hash} mono /><CopyValue label="Contract address" value={anchor.contract_address} mono /></div>
            <div className="flex gap-4 border border-accent/20 bg-accent/5 p-5"><span className="flex size-10 shrink-0 items-center justify-center rounded-md bg-accent/10 text-accent"><LockKeyhole className="size-5" /></span><p className="text-base leading-relaxed"><strong>Privacy by design.</strong> Only hashes, the purpose, and counts are stored on-chain. The document and its PII never touch the chain.</p></div>
            {error?.action === "verify" && <ErrorPanel error={error.message} onRetry={() => retry("verify")} />}
            <div className="flex flex-wrap justify-between gap-3"><Button variant="outline" size="lg" onClick={() => setStep(2)}><ArrowLeft className="size-4" />Back to results</Button><Button size="lg" disabled={busyAction === "verify"} onClick={runVerify}>{busyAction === "verify" ? <LoaderCircle className="size-5 animate-spin" /> : <ShieldCheck className="size-5" />}{busyAction === "verify" ? "Verifying…" : "Verify on-chain record"}<ArrowRight className="size-4" /></Button></div>
          </div>}

          {step === 4 && verification && analysis && anchor && <div className="space-y-7">
            <div><p className="mb-1 text-sm font-semibold text-accent">STEP 04</p><h2 className="text-2xl font-bold sm:text-3xl">Verify the record</h2><p className="mt-1 text-base text-muted-foreground">Compare the original report with what the blockchain returned.</p></div>
            <div className={`flex items-center gap-4 border px-5 py-4 ${recordMatches ? "border-emerald-600/25 bg-emerald-600/5 text-emerald-800" : "border-destructive/25 bg-destructive/5 text-destructive"}`}><span className="flex size-11 shrink-0 items-center justify-center rounded-full bg-card">{recordMatches ? <CheckCircle2 className="size-6" /> : <XCircle className="size-6" />}</span><div><h3 className="text-xl font-bold">{recordMatches ? "Record verified" : "Mismatch detected"}</h3><p className="text-sm opacity-85">{recordMatches ? "The purpose and field counts match the anchored report." : "One or more on-chain values differ from the off-chain report."}</p></div></div>
            <div className="overflow-hidden border border-border bg-card"><div className="grid grid-cols-[1fr_1fr_1fr_48px] border-b border-border bg-muted px-4 py-3 text-xs font-bold uppercase tracking-wide text-muted-foreground sm:px-6"><div>Audit value</div><div>Off-chain report</div><div>On-chain record</div><div className="text-center">Match</div></div>{compareRows.map((row) => <div key={row.label} className="grid grid-cols-[1fr_1fr_1fr_48px] items-center border-b border-border px-4 py-4 text-sm last:border-b-0 sm:px-6 sm:text-base"><span className="font-semibold">{row.label}</span><span className="break-words pr-2 text-muted-foreground">{row.report}</span><span className="break-words pr-2 font-medium">{row.chain}</span><span className="flex justify-center">{row.match ? <CheckCircle2 className="size-5 text-emerald-700" /> : <XCircle className="size-5 text-destructive" />}</span></div>)}</div>
            <div className="grid gap-px overflow-hidden border border-border bg-border sm:grid-cols-2 lg:grid-cols-4"><RecordDetail label="Sender" value={verification.sender} /><RecordDetail label="Recipient" value={verification.recipient} /><RecordDetail label="Override recorded" value={verification.overridden || overriddenTypes.size > 0 ? "Yes" : "No"} /><RecordDetail label="Timestamp" value={new Date(verification.timestamp).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short", timeZone: "UTC" }) + " UTC"} /></div>
            {error?.action === "verify" && <ErrorPanel error={error.message} onRetry={() => retry("verify")} />}
            <div className="flex flex-wrap justify-between gap-3"><Button variant="outline" size="lg" onClick={() => setStep(3)}><ArrowLeft className="size-4" />Back to anchor</Button><Button variant="outline" size="lg" onClick={() => { setStep(1); setUnlockedStep(1); setAnalysis(null); setAnchor(null); setVerification(null); setOverriddenTypes(new Set()); }}><RotateCw className="size-4" />Start a new audit</Button></div>
          </div>}

          {error && !["samples", ...(step === 1 ? ["analyze"] : []), ...(step === 3 ? ["verify"] : []), ...(step === 4 ? ["verify"] : [])].includes(error.action) && <ErrorPanel error={error.message} onRetry={() => retry(error.action)} />}
        </section>
      </main>

      <footer className="border-t border-border bg-card"><div className="mx-auto flex max-w-7xl gap-3 px-5 py-5 text-sm leading-relaxed text-muted-foreground sm:px-8"><AlertCircle className="mt-0.5 size-4 shrink-0 text-accent" /><p>Research prototype. Runs on a local test blockchain (Ganache); not production-ready. OCR on scanned documents is a known weak spot for medical and biometric fields.</p></div></footer>

      <Sheet open={settingsOpen} onOpenChange={setSettingsOpen}><SheetContent className="w-full overflow-y-auto sm:max-w-md"><SheetHeader className="text-left"><SheetTitle className="text-2xl">Demo settings</SheetTitle><SheetDescription>Choose how this prototype connects to the audit service.</SheetDescription></SheetHeader><div className="mt-8 space-y-7 px-1"><div className="flex items-start justify-between gap-5 border-b border-border pb-6"><div className="space-y-1"><Label htmlFor="mock-mode" className="text-base font-semibold">Use mock data</Label><p className="max-w-xs text-sm leading-relaxed text-muted-foreground">When enabled, all sample, audit, and blockchain data stays local. No network requests are made.</p></div><Switch id="mock-mode" checked={settings.mockMode} onCheckedChange={(checked) => { setSettings((current) => ({ ...current, mockMode: checked })); setError(null); }} /></div><div className="space-y-2"><Label htmlFor="api-url">API base URL</Label><Input id="api-url" value={settings.baseUrl} onChange={(event) => setSettings((current) => ({ ...current, baseUrl: event.target.value }))} disabled={settings.mockMode} className="h-11" /><p className="text-sm text-muted-foreground">Used for samples, analysis, anchoring, overrides, and verification.</p></div><div className="border-t border-border pt-5"><h3 className="mb-2 font-semibold">Demo privacy</h3><p className="text-sm leading-relaxed text-muted-foreground">Mock mode does not make API calls. In connected mode, your selected document is sent to the configured audit service for analysis.</p></div></div></SheetContent></Sheet>

      <Dialog open={!!overrideFieldType} onOpenChange={(open) => { if (!open && busyAction !== "override") setOverrideFieldType(null); }}><DialogContent><DialogHeader><DialogTitle>Override {overrideFieldType?.replaceAll("_", " ")}</DialogTitle><DialogDescription>Record why this flagged field should be considered necessary. Your justification is included with the override transaction.</DialogDescription></DialogHeader><div className="space-y-2"><Label htmlFor="override-justification">Justification</Label><textarea id="override-justification" value={overrideJustification} onChange={(event) => setOverrideJustification(event.target.value)} rows={4} placeholder="Explain the specific need for this information…" className="w-full resize-y rounded-md border border-input bg-background px-3 py-2 text-base focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" /></div><DialogFooter><Button variant="outline" onClick={() => setOverrideFieldType(null)}>Cancel</Button><Button disabled={overrideJustification.trim().length < 8 || busyAction === "override"} onClick={submitOverride}>{busyAction === "override" ? <LoaderCircle className="size-4 animate-spin" /> : <Fingerprint className="size-4" />}Record override</Button></DialogFooter></DialogContent></Dialog>

      <div className="sr-only" aria-live="polite">{busyAction ? `${busyAction} in progress` : ""}</div>
    </div>
  );
}

function DocumentPreview({ documentText, selectedValue, documentRef, compact = false }: { documentText: string; selectedValue: string | null; documentRef: React.RefObject<HTMLPreElement | null>; compact?: boolean }) {
  const sections = selectedValue ? documentText.split(new RegExp(`(${escapeRegExp(selectedValue)})`, "ig")) : [documentText];
  return <section className={`overflow-hidden border border-border bg-card ${compact ? "" : "lg:sticky lg:top-6"}`}><div className="flex items-center justify-between border-b border-border px-4 py-3"><div><h3 className="font-semibold">Document text</h3><p className="text-sm text-muted-foreground">{documentText.split(/\s+/).filter(Boolean).length.toLocaleString()} words · Plain text</p></div><span className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground"><LockKeyhole className="size-3.5" />{compact ? "Source document" : "Local preview"}</span></div><pre ref={documentRef} className={`max-h-[610px] overflow-auto whitespace-pre-wrap break-words bg-muted/35 p-5 font-mono text-sm leading-[1.9] text-foreground ${compact ? "max-h-[320px]" : ""}`}>{sections.map((part, index) => selectedValue && part.toLowerCase() === selectedValue.toLowerCase() ? <mark key={index} className="rounded-sm bg-amber-300 px-0.5 text-foreground ring-2 ring-amber-400/70">{part}</mark> : <span key={index}>{part}</span>)}</pre></section>;
}

function SummaryCard({ label, number, icon, tone }: { label: string; number: number; icon: React.ReactNode; tone: "neutral" | AuditStatus }) {
  const color = tone === "flagged" ? "text-destructive" : tone === "review" ? "text-amber-700" : tone === "cleared" ? "text-emerald-700" : "text-primary";
  return <div className="min-h-[116px] bg-card p-4 sm:p-5"><div className={`mb-3 flex items-center gap-2 text-sm font-semibold ${color}`}>{icon}<span>{label}</span></div><div className={`text-3xl font-bold tabular-nums ${color}`}>{number}</div></div>;
}

function FieldRow({ field, selected, overridden, onSelect, onOverride }: { field: AuditField; selected: boolean; overridden: boolean; onSelect: () => void; onOverride: () => void }) {
  const [expanded, setExpanded] = useState(false);
  return <>
    <tr className={`border-b border-border last:border-0 ${selected ? "bg-amber-500/8" : "hover:bg-muted/45"}`}>
      <td className="px-4 py-4 align-top font-semibold capitalize">{field.field_type.replaceAll("_", " ")}</td>
      <td className="max-w-[300px] px-4 py-4 align-top"><button type="button" onClick={onSelect} className="max-w-full break-words text-left text-primary underline decoration-primary/25 underline-offset-4 hover:decoration-primary">{field.value}</button></td>
      <td className="px-4 py-4 align-top"><div className="flex items-center gap-2"><div className="h-2.5 w-20 overflow-hidden rounded-full bg-muted"><div className={`h-full rounded-full ${field.status === "flagged" ? "bg-destructive" : field.status === "review" ? "bg-amber-500" : "bg-emerald-600"}`} style={{ width: `${Math.max(0, Math.min(100, field.N * 100))}%` }} /></div><span className="font-mono text-xs tabular-nums">{field.N.toFixed(2)}</span></div></td>
      <td className="px-4 py-4 align-top"><StatusBadge status={field.status} /></td>
      <td className="px-4 py-3 align-top"><div className="flex items-center gap-1"><Button type="button" variant="ghost" size="icon" className="size-8" title="View score details" aria-label="View score details" onClick={() => setExpanded((current) => !current)}>{expanded ? <ChevronDown className="size-4" /> : <ChevronRight className="size-4" />}</Button>{field.status === "flagged" && <Button type="button" variant={overridden ? "secondary" : "outline"} size="sm" disabled={overridden} onClick={onOverride}>{overridden ? "Recorded" : "Override"}</Button>}</div></td>
    </tr>
    {expanded && <tr className="border-b border-border bg-muted/35"><td colSpan={5} className="px-5 py-4"><div className="mb-2 flex flex-wrap gap-2"><ScoreChip label="Rule score R" value={field.R} /><ScoreChip label="Model score M" value={field.M} /><span className="rounded bg-card px-2.5 py-1 text-xs font-semibold capitalize text-muted-foreground">API status: {field.status}</span></div><p className="max-w-4xl text-sm leading-relaxed text-muted-foreground">{field.justification}</p></td></tr>}
  </>;
}

function ScoreChip({ label, value }: { label: string; value: number }) { return <span className="rounded bg-card px-2.5 py-1 text-xs font-medium">{label} <span className="font-mono font-bold">{value.toFixed(2)}</span></span>; }

function StatusBadge({ status }: { status: AuditStatus }) {
  const styles = status === "flagged" ? "border-destructive/25 bg-destructive/8 text-destructive" : status === "review" ? "border-amber-600/25 bg-amber-500/10 text-amber-800" : "border-emerald-700/25 bg-emerald-600/8 text-emerald-800";
  return <span className={`inline-flex items-center rounded border px-2.5 py-1 text-xs font-bold capitalize ${styles}`}>{status}</span>;
}

function CopyValue({ label, value, mono = true }: { label: string; value: string; mono?: boolean }) {
  async function copy() {
    try { await navigator.clipboard.writeText(value); toast.success(`${label} copied`); }
    catch { toast.error("Copy is unavailable in this browser"); }
  }
  return <div className="flex min-w-0 items-center justify-between gap-3 bg-card p-4 sm:p-5"><div className="min-w-0"><p className="mb-1 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{label}</p><p title={value} className={`truncate text-sm font-semibold ${mono ? "font-mono" : "tabular-nums"}`}>{shortHash(value)}</p></div><Button type="button" variant="ghost" size="icon" className="size-9 shrink-0" aria-label={`Copy ${label}`} title={`Copy ${label}`} onClick={copy}><Copy className="size-4" /></Button></div>;
}

function RecordDetail({ label, value }: { label: string; value: string }) { return <div className="min-w-0 bg-card p-4"><p className="mb-1 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{label}</p><p className="break-words text-sm font-semibold">{value}</p></div>; }

function ErrorPanel({ error, onRetry }: { error: string; onRetry: () => void }) {
  return <div role="alert" className="flex flex-col justify-between gap-3 border border-destructive/25 bg-destructive/5 p-4 sm:flex-row sm:items-center"><div className="flex gap-3"><AlertCircle className="mt-0.5 size-5 shrink-0 text-destructive" /><p className="text-sm leading-relaxed">{error}</p></div><Button variant="outline" size="sm" onClick={onRetry}><RotateCw className="size-4" />Retry</Button></div>;
}

function messageFor(reason: unknown) { return reason instanceof Error ? reason.message : "Something went wrong. Please try again."; }
function shortHash(value: string) { return value.length > 26 ? `${value.slice(0, 11)}…${value.slice(-9)}` : value; }
function escapeRegExp(value: string) { return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }