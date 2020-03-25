
var PUBLIC_URL = '';
var FILENAME   = 'index.html';
var BUNDLEJS   = 'bundle.js';
var INPUT      = `public/${FILENAME}`;
var OUTPUT     = `dist/${FILENAME}`;

var fs = require('fs');

fs.readFile(INPUT, 'utf8', function (err, data) {

	if (err) {
		return console.log(err);
	}

	data = data.replace(/<\/body>/g,
	`
		<script src=${BUNDLEJS}></script>
	</body>
	`
	);
	data = data.replace(/%PUBLIC_URL%/g, PUBLIC_URL);

	fs.writeFile(OUTPUT, data, 'utf8', function (err) {
		if (err) return console.log(err);
	});
});
