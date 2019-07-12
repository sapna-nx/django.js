(function(){

    "use strict";

    function DjangoJsError(message) {
        this.name = "DjangoJsError";
        this.message = (message || "");
    }
    DjangoJsError.prototype = Error.prototype;

    function get(url, callback) {
        var request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.onreadystatechange = function() {
            if (request.readyState == 4 && request.status == 200)
                callback(JSON.parse(request.responseText));
        }
        request.send();
    }

    var Django = window.Django = {

        token_regex: /<\w*>/g,
        named_token_regex: /<(\w+)>/g,

        /**
         * Initialize required attributes
         */
        initialize: function(params) {
            params = params || {};
            if (typeof params.urls === 'string' || params.urls instanceof String) {
                get(params.urls, function(urls) {
                    Django.urls = urls;
                });
            } else {
                this.urls = params.urls || window.DJANGO_JS_URLS;
            }
        },

        /**
         * Equivalent to ``reverse`` function and ``url`` template tag.
         */
        url: function(name, args) {
            var pattern = this.urls[name] || false,
                url = pattern,
                key, regex, token, parts;

            if (!url)
                throw new DjangoJsError('URL for view "' + name + '" not found');

            if (args === undefined)
                return url;

            if (Array.isArray(args))
                return this._url_from_array(name, pattern, args);
            return this._url_from_object(name, pattern, args);
        },

        _url_from_array: function(name, pattern, array) {
            var matches = pattern.match(this.token_regex),
                parts = pattern.split(this.token_regex),
                url = parts[0];

            if (!matches && array.length === 0) {
                return url;
            }

            if (matches && matches.length != array.length) {
                throw new DjangoJsError('Wrong number of argument for pattern "' + name + '"');
            }


            for (var idx=0; idx < array.length; idx++) {
                url += array[idx] + parts[idx + 1];
            }

            return url;
        },

        _url_from_object: function(name, pattern, object) {
            var url = pattern,
                tokens = pattern.match(this.token_regex);

            if (!tokens) {
                return url;
            }

            for (var idx=0; idx < tokens.length; idx++) {
                var token = tokens[idx],
                    prop = token.slice(1, -1),
                    value = object[prop];

                if (value === undefined) {
                    throw new DjangoJsError('Property "' + prop + '" not found');
                }

                url = url.replace(token, value);
            }

            return url;
        },
    };

    return Django;

}());
