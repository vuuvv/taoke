$(function() {
	var workspace = Backbone.Router.extend({
		routes: {
			'hello': 'hello',
			'*url': 'dispatch'
		},

		hello: function() {
			$.dialog('hello');
		},

		dispatch: function(url) {
			if (!url)
				return false;
			$.ajax("/" + url, data={}).done(function(data) {
				$.dialog(data);
					/*
				container = $('#main_content');
				container.html(data)
				*/
			});
			//return false;
		}
	});

	app = new workspace();

	Backbone.history.start();

	$.fn.toggle_click = function(first, second) {
		var ele = this,
			name = 'click_state';
		ele.data(name, 0);
		ele.click(function() {
			if (ele.data('click_state'))
				second()
			else
				first()
			ele.data(name, !ele.data(name));
			return false;
		});
	};
	var set_height = function() {
		var doc_height = document.documentElement.clientHeight;
		$('#main_content').height(doc_height - 80);
		$('#left_toggle').height(doc_height - 52);
		$('body').css('overflow', 'hidden');
	}

	set_height();

	$(window).resize(set_height);

	$('#left_toggle').toggle_click(function() {
		$('html').addClass('close');
		$('.left_side').addClass('left_side_off');
		$('#left_toggle').removeClass('left_hide');
		$('#left_toggle').addClass('left_show');
	}, function() {
		$('html').removeClass('close');
		$('.left_side').removeClass('left_side_off');
		$('#left_toggle').removeClass('left_show');
		$('#left_toggle').addClass('left_hide');
	});

	$(document).ajaxStart(function() {
		$('#ajax_loading').show();
	}).ajaxSuccess(function() {
		$('#ajax_loading').hide();
	});
});

