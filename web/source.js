(function () {
    function drawStrokeText(ctx, text, x, y,width) {
        ctx.font = '24pt Calibri';
        ctx.miterLimit = 2;
        ctx.textAlign = 'center';
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 12;
        ctx.strokeText(text, x, y,width);
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
            canvas = document.getElementById('display'),
            topcanvas = document.getElementById('top'),
            bottomcanvas = document.getElementById('bottom'),
            ctx = canvas.getContext('2d'),
            topctx = topcanvas.getContext('2d'),
            bottomctx = bottomcanvas.getContext('2d'),
            socket = new ReconnectingWebSocket('ws://' + params.websocketserver + ':' + params.websockport);

        var heartbeatInterval = null,
            missedHeartbeats = 0,
            ginputdelay = 0,
            display = new SegmentDisplay("display"),
            backgroundColor = params.background,
            onColor = params.oncolor,
            offColor = params.offcolor;
            
        if(!onColor){
            onColor = "#24dd22";
        }
        if(!offColor){
            offColor = "#1F4905";
        }
        if(!backgroundColor){
            backgroundColor = "Black";
        }
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        display.displayAngle    = 5;
        display.digitHeight     = 20;
        display.digitWidth      = 15;
        display.digitDistance   = 2.5;
        display.segmentWidth    = 2;
        display.segmentDistance = 0.5;
        display.segmentCount    = 14;
        display.cornerType      = 3;
        display.colorOn         = onColor;
        display.colorOff        = offColor;
        display.pattern         = "##.#######";
        display.draw();
        display.setValue("-1.502  kΩ");
        canvas.style.background = backgroundColor;
        topcanvas.style.background = backgroundColor;
        bottomcanvas.style.background = backgroundColor;
        bottomctx.font = "italic bold 14pt Arial";
        bottomctx.fillStyle = display.colorOn;
        bottomctx.fillText("MP730026 BLE DMM",62,18);
        
        topctx.font = "bold 16pt Arial";
        topctx.fillStyle = display.colorOn;
        
        topctx.fillText("HOLD",61,18);
        topctx.fillStyle = display.colorOff;
        topctx.fillText("REL",190,18);
        socket.onopen = (event) => {
            console.log('Connected to: ' + event.currentTarget.url);
        };
        window.onunload = () => {
            socket.close();
        };
        socket.onmessage = (event) => {
            console.log(event.data);
            let dataReg = /(.*) (.*) (.*) (.*)/,
                patternReg = /[\-0-9]/g,
                zeroReg = /(?<![\.1-9])0(?!$)/g,
                value = '',
                pattern = '';
                
                
            switch (event.data) {
                case 'Connected':
                    return;
            }
            //Get matched values
            let patternMatch = event.data.match(dataReg);
            //Replace leading zeros with spaces
            value = patternMatch[3].replace(zeroReg,"");
            //Turn Value into Mask for LCD Padding to 9 long
            pattern = value.replace(patternReg,"#").padStart(6,"#");
            //Append Suffix with padding for justification
            
            value = value + patternMatch[4].padStart(3," ");
            console.log(value)
            
            //Add additional Spots for Suffix
            display.pattern = pattern + "###";
            display.draw();
            display.setValue(value.padStart(9," "));
            
            console.log(pattern);
           
            
            
        };
    };
})();
