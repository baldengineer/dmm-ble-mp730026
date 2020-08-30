(function () {
    function drawStrokeText(ctx, text, x, y, width) {
        ctx.font = '24pt Calibri';
        ctx.miterLimit = 2;
        ctx.textAlign = 'center';
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 12;
        ctx.strokeText(text, x, y, width);
        ctx.fillStyle = 'white';
        ctx.fillText(text, x, y, width);
    }
    // Graciously stolen from sitepoint
    // https://www.sitepoint.com/get-url-parameters-with-javascript/
    function getAllUrlParams(url) {
        // get query string from url (optional) or window
        var queryString = url ? url.split('?')[1] : window.location.search.slice(1);

        // we'll store the parameters here
        var obj = {};

        // if query string exists
        if (queryString) {
            // stuff after # is not part of query string, so get rid of it
            queryString = queryString.split('#')[0];

            // split our query string into its component parts
            var arr = queryString.split('&');

            for (var i = 0; i < arr.length; i++) {
                // separate the keys and the values
                var a = arr[i].split('=');

                // in case params look like: list[]=thing1&list[]=thing2
                var paramNum;
                var paramName = a[0].replace(/\[\d*\]/, function (v) {
                    paramNum = v.slice(1, -1);
                    return '';
                });

                // set parameter value (use 'true' if empty)
                var paramValue = typeof (a[1]) === 'undefined' ? true : a[1];

                // (optional) keep case consistent
                paramName = paramName.toLowerCase();
                paramValue = paramValue.toLowerCase();

                // if parameter name already exists
                if (obj[paramName]) {
                    // convert value to array (if still string)
                    if (typeof obj[paramName] === 'string') {
                        obj[paramName] = [obj[paramName]];
                    }
                    // if no array index number specified...
                    if (typeof paramNum === 'undefined') {
                        // put the value on the end of the array
                        obj[paramName].push(paramValue);
                    }
                    // if array index number specified...
                    else {
                        // put the value at that index number
                        obj[paramName][paramNum] = paramValue;
                    }
                }
                // if param name doesn't exist yet, set it
                else {
                    obj[paramName] = paramValue;
                }
            }
        }
        return obj;
    }
    window.onload = async () => {
        const ReconnectingWebSocket = require('reconnecting-websocket'),
            params = getAllUrlParams(),
            topcanvas = document.getElementById('top'),
            bottomcanvas = document.getElementById('bottom'),
            frontcanvas = document.getElementById('front'),
            backcanvas = document.getElementById('back'),
            char1canvas = document.getElementById('display1'),
            char2canvas = document.getElementById('display2'),
            char3canvas = document.getElementById('display3'),
            char4canvas = document.getElementById('display4'),
            topctx = topcanvas.getContext('2d'),
            bottomctx = bottomcanvas.getContext('2d'),
            frontctx = frontcanvas.getContext('2d'),
            backctx = backcanvas.getContext('2d'),
            char1ctx = char1canvas.getContext('2d'),
            char2ctx = char2canvas.getContext('2d'),
            char3ctx = char3canvas.getContext('2d'),
            char4ctx = char4canvas.getContext('2d'),
            socket = new ReconnectingWebSocket('ws://' + params.websocketserver + ':' + params.websocketport + '/live/' + params.meter);

        var heartbeatInterval = null,
            missedHeartbeats = 0,
            ginputdelay = 0,
            char1 = new SegmentDisplay("display1"),
            char2 = new SegmentDisplay("display2"),
            char3 = new SegmentDisplay("display3"),
            char4 = new SegmentDisplay("display4"),
            backgroundColor = params.background,
            onColor = params.oncolor,
            offColor = params.offcolor,
            display_string = params.displaytxt;

        if (!onColor) {
            onColor = "#24dd22";
        }
        if (!offColor) {
            offColor = "#1F4905";
        }
        if (!backgroundColor) {
            backgroundColor = "Black";
        }
        if (!display_string) {
            display_string = "MP730026 BLE DMM"
        }

        char1.displayAngle = 5;
        char1.digitHeight = 20;
        char1.digitWidth = 15;
        char1.digitDistance = 2.5;
        char1.segmentWidth = 2;
        char1.segmentDistance = 0.5;
        char1.segmentCount = 14;
        char1.cornerType = 3;
        char1.colorOn = onColor;
        char1.colorOff = offColor;
        char1.pattern = "#";
        char1.draw();

        char2.displayAngle = 5;
        char2.digitHeight = 20;
        char2.digitWidth = 15;
        char2.digitDistance = 2.5;
        char2.segmentWidth = 2;
        char2.segmentDistance = 0.5;
        char2.segmentCount = 14;
        char2.cornerType = 3;
        char2.colorOn = onColor;
        char2.colorOff = offColor;
        char2.pattern = "#";
        char2.draw();

        char3.displayAngle = 5;
        char3.digitHeight = 20;
        char3.digitWidth = 15;
        char3.digitDistance = 2.5;
        char3.segmentWidth = 2;
        char3.segmentDistance = 0.5;
        char3.segmentCount = 14;
        char3.cornerType = 3;
        char3.colorOn = onColor;
        char3.colorOff = offColor;
        char3.pattern = "#";
        char3.draw();

        char4.displayAngle = 5;
        char4.digitHeight = 20;
        char4.digitWidth = 15;
        char4.digitDistance = 2.5;
        char4.segmentWidth = 2;
        char4.segmentDistance = 0.5;
        char4.segmentCount = 14;
        char4.cornerType = 3;
        char4.colorOn = onColor;
        char4.colorOff = offColor;
        char4.pattern = "#";
        char4.draw();

        document.getElementById("display").style.background = backgroundColor;

        bottomctx.font = "italic bold 14pt Arial";
        bottomctx.fillStyle = onColor;
        bottomctx.textAlign = "center";
        bottomctx.fillText(unescape(display_string), bottomcanvas.width / 2, bottomcanvas.height - 4, 250);
        char1.setValue("");
        char2.setValue("");
        char3.setValue("");
        char4.setValue("");
        topctx.font = "16pt Arial";
        topctx.fillStyle = offColor;
        topctx.fillText("HOLD", 30, 18);
        topctx.fillText("REL", 100, 18);
        topctx.fillText("AUTO", 153, 18);
        frontctx.font = "italic bold 38pt Arial";
        frontctx.fillStyle = char1.colorOff;
        frontctx.fillText("-", 5, 33);
        socket.onopen = (event) => {
            console.log('Connected to: ' + event.currentTarget.url);
        };
        window.onunload = () => {
            socket.close();
        };
        socket.onmessage = (event) => {
            // console.log(event.data);

            switch (event.data) {
                case 'Connected':
                    return;
            }
            let DMM = JSON.parse(event.data);
            if (!DMM.value) {
                char1.setValue("");
                char2.setValue("");
                char3.setValue("");
                char4.setValue("");
                DMM.suffix = "";
            } else if (DMM.value == "O.L") {
                char1.setValue("");
                char2.setValue("o");
                char3.setValue("l");
                char4.setValue("");
                DMM.decimal = 2;
            } else {
                let value = DMM.value.replace(".", "")
                value = value.replace("-", "")
                char1.setValue(value.charAt(0));
                char2.setValue(value.charAt(1));
                char3.setValue(value.charAt(2));
                char4.setValue(value.charAt(3));
            }
            frontctx.clearRect(0, 0, frontcanvas.width, frontcanvas.height);
            frontctx.font = "italic bold 38pt Arial";
            frontctx.fillStyle = char1.colorOff;
            if (DMM.negative == true) {
                frontctx.fillStyle = char1.colorOn;
            }
            frontctx.fillText("-", 5, 33);

            topctx.clearRect(0, 0, topcanvas.width, topcanvas.height);

            if (DMM.low_battery == true) {
                topctx.font = "16pt Arial";
                topctx.fillStyle = char1.colorOn;
                topctx.fillText("🗲", 5, 18);
            }


            topctx.font = "16pt Arial";
            topctx.fillStyle = char1.colorOff;
            if (DMM.hold == true) {
                topctx.fillStyle = char1.colorOn;
            }
            topctx.fillText("HOLD", 30, 18);

            topctx.font = "16pt Arial";
            topctx.fillStyle = char1.colorOff;
            if (DMM.rel == true) {
                topctx.fillStyle = char1.colorOn;
            }
            topctx.fillText("REL", 100, 18);

            topctx.font = "16pt Arial";
            topctx.fillStyle = char1.colorOff;
            if (DMM.autorange == true) {
                topctx.fillStyle = char1.colorOn;
            }

            topctx.fillText("AUTO", 153, 18);

            backctx.clearRect(0, 0, backcanvas.width, backcanvas.height);
            backctx.font = "28pt Arial";
            backctx.fillStyle = char1.colorOn;
            backctx.fillText(DMM.suffix, 0, 40, 50)

            switch (DMM.decimal) {
                case 1:
                    char1ctx.fillStyle = char1.colorOn;
                    char2ctx.fillStyle = char1.colorOff;
                    char3ctx.fillStyle = char1.colorOff;
                    char4ctx.fillStyle = char1.colorOff;
                    break;
                case 2:
                    char1ctx.fillStyle = char1.colorOff;
                    char2ctx.fillStyle = char1.colorOn;
                    char3ctx.fillStyle = char1.colorOff;
                    char4ctx.fillStyle = char1.colorOff;
                    break;
                case 3:
                    char1ctx.fillStyle = char1.colorOff;
                    char2ctx.fillStyle = char1.colorOff;
                    char3ctx.fillStyle = char1.colorOn;
                    char4ctx.fillStyle = char1.colorOff;
                    break;
                case 4:
                    char1ctx.fillStyle = char1.colorOff;
                    char2ctx.fillStyle = char1.colorOff;
                    char3ctx.fillStyle = char1.colorOff;
                    char4ctx.fillStyle = char1.colorOn;
                    break;
                default:
                    char1ctx.fillStyle = char1.colorOff;
                    char2ctx.fillStyle = char1.colorOff;
                    char3ctx.fillStyle = char1.colorOff;
                    char4ctx.fillStyle = char1.colorOff;

            }
            char1ctx.fillRect(35, 35, 3, 5);
            char2ctx.fillRect(35, 35, 3, 5);
            char3ctx.fillRect(35, 35, 3, 5);
            char4ctx.fillRect(35, 35, 3, 5);
        };
    };
})();
