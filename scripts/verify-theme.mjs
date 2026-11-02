import { chromium } from "playwright";

const url = process.env.SITE_URL ?? "https://jtirado5933.github.io/cca-f-study-prompts/";
const expected = {
  titleIncludes: "Copy/Paste Prompts",
  bodyBg: "rgb(13, 19, 41)",
  t3Blue: "#24b1e6",
  linkRgb: "rgb(22, 128, 182)",
  noPlaceholder: true,
};

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(url, { waitUntil: "networkidle" });

const title = await page.title();
const sample = await page.evaluate(() => {
  const root = getComputedStyle(document.documentElement);
  const link = document.querySelector("article a");
  return {
    bodyBg: getComputedStyle(document.body).backgroundColor,
    t3Blue: root.getPropertyValue("--t3-blue").trim(),
    linkColor: link ? getComputedStyle(link).color : "",
    hasPlaceholder: document.body.textContent.includes("[PLACEHOLDER"),
    h1: document.querySelector("h1")?.textContent ?? "",
  };
});

await browser.close();

const failures = [];
if (!title.includes(expected.titleIncludes)) failures.push(`title: ${title}`);
if (sample.bodyBg !== expected.bodyBg) failures.push(`body bg: ${sample.bodyBg} (want ${expected.bodyBg})`);
if (sample.t3Blue !== expected.t3Blue) failures.push(`--t3-blue: ${sample.t3Blue}`);
if (sample.linkColor !== expected.linkRgb) failures.push(`link: ${sample.linkColor}`);
if (expected.noPlaceholder && sample.hasPlaceholder) failures.push("page still has PLACEHOLDER text");
if (sample.h1.includes("Study Prompts") && !sample.h1.includes("Prep")) failures.push(`stale h1: ${sample.h1}`);

if (failures.length) {
  console.error("Theme check FAILED:\n" + failures.map((f) => `  - ${f}`).join("\n"));
  process.exit(1);
}
console.log("Theme check OK:", url);
