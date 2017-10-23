function doAddTags(tag1,tag2,obj) {
	textarea = document.getElementById(obj);

	var len = textarea.value.length;
	var start = textarea.selectionStart;
	var end = textarea.selectionEnd;
				
	var scrollTop = textarea.scrollTop;
	var scrollLeft = textarea.scrollLeft;
	
    var sel = textarea.value.substring(start, end);
	var rep = tag1 + sel + tag2;
    textarea.value =  textarea.value.substring(0,start) + rep + textarea.value.substring(end,len);
		
	textarea.scrollTop = scrollTop;
	textarea.scrollLeft = scrollLeft;
		
}
