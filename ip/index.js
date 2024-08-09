const launch = require("puppeteer-core").launch;
const ArgumentParser = require("argparse").ArgumentParser;

const parser = new ArgumentParser();

parser.add_argument("url", { help: "the url to visit" });

const args = parser.parse_args();

async function main() {
	const browser = await launch({
		executablePath: "/usr/bin/chromium-browser",
	});

	const [page] = await browser.pages();

	await page.goto(args.url);

	await page.waitForSelector("input[name=username]");

	await page.$eval(
		"input[name=username]",
		(el) => (el.value = "ahmedelbehairy@mafazaa.com")
	);
	await page.$eval(
		"input[name=password]",
		(el) => (el.value = "@Hm258191825")
	);

	await page.click('input[type="submit"]');

	await page.close();
}

main();
