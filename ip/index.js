const launch = require("puppeteer-core").launch;
const ArgumentParser = require("argparse").ArgumentParser;

const parser = new ArgumentParser();

parser.add_argument("url", { help: "the url to visit" });
parser.add_argument("email", { help: "the email to sign in with" });
parser.add_argument("password", { help: "the password for signing in" });

const args = parser.parse_args();

async function main() {
	const browser = await launch({
		executablePath: "/usr/bin/chromium-browser",
	});

	const [page] = await browser.pages();

	await page.goto(args.url);

	await page.waitForSelector("input[name=username]");

	await page.$eval("input[name=username]", (el) => (el.value = args.email));
	await page.$eval(
		"input[name=password]",
		(el) => (el.value = args.password)
	);

	await page.click('input[type="submit"]');

	await page.close();
}

main();
