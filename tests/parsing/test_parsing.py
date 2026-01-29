# /// script
# dependencies = [
#     "pytools
# ]
# ///
from pytools.parsing import ppfmt

benchmark = r"""{
  name: example,
  values: [
    1,
    2,
    3,
    {
      nested: [
        4,
        5,
        6,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        23,
        12,
        13,
        100,
        14,
        15,
        16,
        seventeen,
        eighteen,
        nineteen,
        twenty,
        {deeply_nested: [0, 1, 2, 3, 4, 5]}
      ]
    }
  ],
  details: {
    description: A sample data structure,
    tags: [sample, test, data],
    metadata: {created_by: user, version: 1.0},
    empty_list: []
  }
}"""


def test_format_collection() -> None:
    data = {
        "name": "example",
        "values": [
            1,
            2,
            3,
            {
                "nested": [
                    4,
                    5,
                    6,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    23,
                    12,
                    13,
                    100,
                    14,
                    15,
                    "16",
                    "seventeen",
                    "eighteen",
                    "nineteen",
                    "twenty",
                    {"deeply_nested": list(range(6))},
                ]
            },
        ],
        "details": {
            "description": "A sample data structure",
            "tags": ["sample", "test", "data"],
            "metadata": {"created_by": "user", "version": 1.0},
            "empty_list": [],
        },
    }

    formatted = ppfmt(data)

    assert formatted == benchmark
