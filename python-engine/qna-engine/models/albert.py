import os
import torch
import time
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler

from transformers import (
    AlbertConfig,
    AlbertForQuestionAnswering,
    AlbertTokenizer,
    squad_convert_examples_to_features,
)

from transformers.data.processors.squad import (
    SquadResult,
    SquadV2Processor,
    SquadExample,
)

from transformers.data.metrics.squad_metrics import compute_predictions_logits


class Albert():
    def __init__(
        self,
        model_name_or_path = "ktrapeznikov/albert-xlarge-v2-squad-v2",
        n_best_size = 1,
        max_answer_length = 30,
        do_lower_case = True,
        null_score_diff_threshold = 0.0,
    ):
        self.n_best_size = n_best_size
        self.max_answer_length = max_answer_length
        self.do_lower_case = do_lower_case
        self.null_score_diff_threshold = null_score_diff_threshold
        self.config_class = AlbertConfig
        self.model_class = AlbertForQuestionAnswering
        self.tokenizer_class = AlbertTokenizer
        self.config = self.config_class.from_pretrained(model_name_or_path)
        self.tokenizer = self.tokenizer_class.from_pretrained(
            model_name_or_path, do_lower_case=self.do_lower_case
        )
        self.model = self.model_class.from_pretrained(
            model_name_or_path, config=self.config
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.processor = SquadV2Processor()

    def _to_list(self, tensor):
        return tensor.detach().cpu().tolist()

    def infer(self, context_text, question_texts):
        """Setup function to compute predictions"""
        examples = []

        for i, question_text in enumerate(question_texts):
            example = SquadExample(
                qas_id=str(i),
                question_text=question_text,
                context_text=context_text,
                answer_text=None,
                start_position_character=None,
                title="Predict",
                is_impossible=False,
                answers=None,
            )

            examples.append(example)

        features, dataset = squad_convert_examples_to_features(
            examples=examples,
            tokenizer=self.tokenizer,
            max_seq_length=384,
            doc_stride=128,
            max_query_length=64,
            is_training=False,
            return_dataset="pt",
            threads=1,
        )

        eval_sampler = SequentialSampler(dataset)
        eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=10)

        all_results = []

        for batch in eval_dataloader:
            self.model.eval()
            batch = tuple(t.to(self.device) for t in batch)

            with torch.no_grad():
                inputs = {
                    "input_ids": batch[0],
                    "attention_mask": batch[1],
                    "token_type_ids": batch[2],
                }

                example_indices = batch[3]

                outputs = self.model(**inputs)

                for i, example_index in enumerate(example_indices):
                    eval_feature = features[example_index.item()]
                    unique_id = int(eval_feature.unique_id)

                    output = [self._to_list(output[i]) for output in outputs]

                    start_logits, end_logits = output
                    result = SquadResult(unique_id, start_logits, end_logits)
                    all_results.append(result)

        output_prediction_file = "predictions.json"
        output_nbest_file = "nbest_predictions.json"
        output_null_log_odds_file = "null_predictions.json"

        predictions = compute_predictions_logits(
            examples,
            features,
            all_results,
            self.n_best_size,
            self.max_answer_length,
            self.do_lower_case,
            output_prediction_file,
            output_nbest_file,
            output_null_log_odds_file,
            False,  # verbose_logging
            True,  # version_2_with_negative
            self.null_score_diff_threshold,
            self.tokenizer,
        )

        return predictions


if __name__ == "__main__":
    albert = Albert()
    context = "New Zealand (Māori: Aotearoa) is a sovereign island country in the southwestern Pacific Ocean. It has a total land area of 268,000 square kilometres (103,500 sq mi), and a population of 4.9 million. New Zealand's capital city is Wellington, and its most populous city is Auckland."
    questions = ["How many people live in New Zealand?", "What's the largest city?"]
    predictions = albert.infer(context, questions)

    for key in predictions.keys():
        print(predictions[key])
