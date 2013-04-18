$(function() {
	var ajax_failed_tip = function(jqxhr) {
		var parts = jqxhr.responseText.split('\n');
		$.dialog({
			title: parts[0],
			content: parts[1]
		});
	};

	var workspace = Backbone.Router.extend({
		routes: {
			'hello': 'hello',
			'*url': 'dispatch'
		},

		hello: function() {
			$.dialog('hello');
		},

		dispatch: function(url) {
			var me = this;
			if (!url)
				return false;
			$.ajax({
				url: "/" + url,
				data: {},
				dataType: 'json',
			}).done(function(data) {
				if (data.success)
					me.add_tab(data.id, data.title, data.content);
			}).fail(function(jqxhr, status) {
				ajax_failed_tip(jqxhr);
			});
		},

		add_tab: function(id, label, content) {
			var mtab = $('#mtab'),
				container = $('#main_content');

			mtab.find('li.current').removeClass('current');
			mtab.append(
				'<li class="current"><span><a>'
				+ label + 
				'</a>' +
				'<a title="关闭此页" class="del">关闭</a>' +
				'</span></li>');
			if (this.$page)
				this.$page.hide();
			this.$page = $('<div class="tabpage">' + content + '</div>')
			container.append(this.$page);
		},

		active_tab: function(id) {
		},

		refresh: function() {
			Backbone.history.fragment = null;
			Backbone.history.navigate(document.location.hash, true);
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

	$('#refresh').click(function() {
		app.refresh();
		return false;
	});

	$('#main_content').on('click', '.showdialog', function() {
		var me = $(this),
			title = me.attr('data-title'),
			url = me.attr('href'),
			width = parseInt(me.attr('data-width')),
			height = parseInt(me.attr('data-height'));

		$.ajax(url, data={_popup: true}).done(function(data) {
			$.dialog({
				title: title,
				width: width ? width : 'auto',
				height: height ? height : 'auto',
				padding: '',
				lock: true,
				content: data,
				ok: function() {
					var form = this.dom.content.find('form');
					$.ajax({
						type: 'POST',
						url: url,
						data: form.serialize(),
						dataType: 'json'
					}).done(function(data) {
						if (!data.success) {
							var html = "";
							for (field in data.errors)
								html += 'field:' + field + ', error:' + data.errors[field] + '\n';
							alert(html)
						}
					}).fail(function(jqxhr, status) {
						ajax_failed_tip(jqxhr);
					});
				},
				cancel: function() {}
			});
		});
		return false;
	});
});

