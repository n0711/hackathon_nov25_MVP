# Known issues (WIP)

At the moment the full pytest suite does not pass. The main known issue is:

- `tests/test_determinism.py::test_recommender_deterministic_sort`
  - Fails because `learntwin.Recommender` is not yet fully wired for deterministic
    behaviour and default arguments (`bkt`, `catalog`).
  - The public API has been stabilised so imports work, but the internals still
    need work to satisfy this test.

These are good entry points for contributors who want to work on the recommender
and determinism behaviour.
