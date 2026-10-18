/* START  Toggle Dropdown - English */
const language_english = document.querySelector(".language-english")
if (language_english) {
    language_english.addEventListener("click", function () {
        let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (!segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0] + "-en";
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
    });
}

/* END Toggle Dropdown - English */


/* START  Toggle Dropdown - Chinese */
const language_chinese = document.querySelector(".language-chinese")
if(language_chinese){
	document.querySelector(".language-chinese").addEventListener("click",function() {
		let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0];
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
	})
}
/* END Toggle Dropdown - Chinese */

/* START  Toggle Dropdown - Indonesia */
const language_bahasa = document.querySelector(".language-bahasa")
if(language_bahasa){
	document.querySelector(".language-bahasa").addEventListener("click",function() {
		let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0];
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
	})
}
/* END Toggle Dropdown - Indonesia */

/* START  Toggle Dropdown - Thailand */
const language_thai = document.querySelector(".language-thai");
if(language_thai){
	document.querySelector(".language-thai").addEventListener("click",function() {
		let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0];
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
	})
}
/* END Toggle Dropdown - Thailand */

/* START  Toggle Dropdown - Vietnam */
const language_vietnamese = document.querySelector(".language-vietnamese");

if (language_vietnamese) {
    language_vietnamese.addEventListener("click", function () {
        let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0];
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
    });
}
/* END Toggle Dropdown - Vietnam */

/* START  Toggle Dropdown - All Languages */
const language_md_english = document.querySelector(".language-md-english");
if(language_md_english){
	document.querySelector(".language-md-english").addEventListener("click",function() {
	 	let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (!segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0] + "-en";
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
	})
}

const language_md_chinese = document.querySelector(".language-md-chinese");
if(language_md_chinese){
	document.querySelector(".language-md-chinese").addEventListener("click",function() {
		let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0];
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
	})
}
const language_md_bahasa = document.querySelector(".language-md-bahasa");
if(language_md_bahasa){
	document.querySelector(".language-md-bahasa").addEventListener("click",function() {
		let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0];
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
	})
}
const language_md_thai = document.querySelector(".language-md-thai");
if(language_md_thai){
	document.querySelector(".language-md-thai").addEventListener("click",function() {
		let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0];
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
	})
}
const language_md_vietnamese = document.querySelector(".language-md-vietnamese");
if(language_md_vietnamese){
	document.querySelector(".language-md-vietnamese").addEventListener("click",function() {
		let url = new URL(window.location.href);
        let pathParts = url.pathname.split("/");

        let segmentIndex;

        if (url.pathname.includes("/revamp/") || url.pathname.includes("/revampredirect")) {
            segmentIndex = 2;  
        } else {
            segmentIndex = 1;
        }

        let segmentname = pathParts[segmentIndex];

        if (segmentname.includes("-en")) {
            pathParts[segmentIndex] = segmentname.split("-")[0];
        }

        url.pathname = pathParts.join("/");

        window.location.href = url.toString();

        return false;
	})	
}
/* END Toggle Dropdown - All Languages */