$(document).ready(function (e) {


	$('#btn_corrigir').click(function (e) {
		question = $('#question').val();
		target = $('#target').val();
		answer = $('#answer').val();
		$.ajax({
				url: "/api_get_result",
				type: 'post',
				data: {
					question: question,
					target: target,
					answer: answer,
				},
				beforeSend: function () {
					$("#modal").addClass("loading");
					$('.result-container').hide()
					$('#show-details').hide()
					$('#div-details').hide()
				}
			})
			.done(function (jsondata) {
				response = jsondata["response"]
				console.log(response)

				$('#u_question_target').val(response['u_question_x_target']);
				$('#u_question_answer').val(response['u_question_x_answer']);
				$('#u_answer_target').val(response['u_answer_x_target']);

				$('#roberta_question_target').val(response['r_question_x_target']);
				$('#roberta_question_answer').val(response['r_question_x_answer']);
				$('#roberta_answer_target').val(response['r_answer_x_target']);

				$('#r_contradicao').val(response['r_contradicao']);
				$('#r_neutro').val(response['r_neutro']);
				$('#r_implicacao').val(response['r_implicacao']);

				$('#result-text').html(response['msg'])
				$("#modal").removeClass("loading");

				status = response['status']
				$('#result-text').removeClass()
				if (status == 0)
					$('#result-text').addClass('status_0')

				else if (status == 1)
					$('#result-text').addClass('status_1')

				else if (status == -1)
					$('#result-text').addClass('status_minus')

				$('.result-container').show()
				$('#show-details').show()
			})
			.fail(function (jqXHR, textStatus, jsondata) {
				alert(textStatus);
				console.log(jsondata);
			})
	});

	$('#show-details').click(function (e) {
		$('#div-details').slideToggle(500)
	})

})