const launch = require("puppeteer-core").launch;
const ArgumentParser = require("argparse").ArgumentParser;

const parser = new ArgumentParser();

parser.add_argument("url", { help: "the url to visit" });
parser.add_argument("username", { help: "the email of the opendns account" });
parser.add_argument("password", { help: "password of opendns account" });

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
		(el, username) => (el.value = username),
		args.username
	);
	await page.$eval(
		"input[name=password]",
		(el, password) => (el.value = password),
		args.password
	);

	await page.click('input[type="submit"]');

	await page.waitForNavigation({
		waitUntil: "networkidle2",
	});

	await page.close();
}

main();
