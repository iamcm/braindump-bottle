

	Slideshow = {
		currentPic: 0,
		arrPics: [],
		lenArrPics: 0,
		picTimout: 0,
		nextPic: function () {
			$(this.arrPics[this.currentPic]).fadeOut(1000);
			this.showPic();
		},
		showPic: function () {
			this.currentPic = this.currentPic + 1;
			if (this.currentPic == this.lenArrPics) this.currentPic = 0;
			var el = $(this.arrPics[this.currentPic]);
			el.fadeIn(1000);
			
			//
			el.parent().height($(this.arrPics[this.currentPic]).height());
			//
		},
		init: function (arrEls) {
			this.arrPics = arrEls;
			this.lenArrPics = arrEls.length;
			var self = this;
			setInterval(function(){self.nextPic.call(self);},5000);
			var el = $(this.arrPics[this.currentPic]);
			el.show('1', function(){
				el.parent().height(el.height());
			});
		}
	}
	Slideshow.init($('#slideshowholder img')); 





