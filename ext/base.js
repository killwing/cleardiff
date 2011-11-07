function getSelectedText() {
    if (window.getSelection) {
        return window.getSelection().toString();
    } else if (document.getSelection) {
        return document.getSelection();
    } else if (document.selection) {
        return document.selection.createRange().text;
    }
}

function highlightKeywords(obj, keywords) {
    for (var i = 0; i < keywords.length; i++) {
        var reg = new RegExp('\\b'+keywords[i]+'\\b'+"(?=[^<>]*<)", "g");
        var data = $(obj).html();
        $(obj).html(data.replace(reg, '<span class="keyword">' + keywords[i] + '</span>'));
    }
}

// c++ keywords
var cppkeywords = 
['and','default','template'
,'and_eq','delete','not','this'
,'double','not_eq'
,'asm','dynamic_cast','throw'
,'auto','else','operator','true'
,'bitand','enum','or','try'
,'bitor','explicit','todo','or_eq','typedef'
,'bool','export','private','typeid'
,'break','extern','todo','protected','typename'
,'case','false','public','union'
,'catch','float','register','using'
,'char','for','reinterpret_cast','unsigned'
,'friend','return','void'
,'goto','short','wchar_t'
,'class','if','signed','virtual'
,'compl','inline','sizeof','volatile'
,'const','int','static','while'
,'long','xor'
,'const_cast','mutable','static_cast','xor_eq'
,'continue','namespace','struct'
,'new','switch'];

