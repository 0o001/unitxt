import datasets as ds
from src.unitxt import dataset
from src.unitxt.blocks import (
    AddFields,
    FormTask,
    InputOutputTemplate,
    LoadHF,
    MapInstanceValues,
    NormalizeListFields,
    SplitRandomMix,
    TaskCard,
    TemplatesList,
)
from src.unitxt.catalog import add_to_catalog
from src.unitxt.operators import RenameFields
from src.unitxt.splitters import RenameSplits
from src.unitxt.test_utils.card import test_card

default_splitter = SplitRandomMix({"train": "train", "validation": "validation", "test": "test"})
add_to_catalog(default_splitter, "splitters.default", overwrite=True)

card = TaskCard(
    loader=LoadHF(path="glue", name="qnli"),
    preprocess_steps=[
        "splitters.large_no_test",
        MapInstanceValues(mappers={"label": {"0": "entailment", "1": "not entailment"}}),
        AddFields(
            fields={
                "choices": ["entailment", "not entailment"],
            }
        ),
        RenameFields(
            field_to_field={
                "question": "premise",
                "sentence": "hypothesis",
            }
        ),
    ],
    task="tasks.nli",
    templates="templates.nli",
)

test_card(card)
add_to_catalog(card, "cards.qnli", overwrite=True)
