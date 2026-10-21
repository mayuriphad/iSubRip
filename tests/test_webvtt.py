import datetime as dt

import pytest

from isubrip.subtitle_formats.webvtt import WebVTTCaptionBlock


def _block(payload: str, settings: str = "") -> WebVTTCaptionBlock:
    return WebVTTCaptionBlock(
        start_time=dt.time(0, 0, 1),
        end_time=dt.time(0, 0, 2),
        payload=payload,
        settings=settings,
    )


class TestToSrtCharacterReferences:
    @pytest.mark.parametrize(
        ("payload", "expected"),
        [
            ("Tom &amp; Jerry", "Tom & Jerry"),
            ("1 &lt; 2 &gt; 0", "1 < 2 > 0"),
            ("a&nbsp;b", "a\u00a0b"),
            ("&rlm;Hello", "\u200fHello"),
            # An escaped ampersand must not be unescaped a second time.
            ("&amp;amp;", "&amp;"),
            ("<i>Fish &amp; chips</i>", "<i>Fish & chips</i>"),
            ("No references here", "No references here"),
        ],
    )
    def test_references_are_unescaped(self, payload: str, expected: str) -> None:
        assert _block(payload).to_srt().payload == expected

    def test_references_are_unescaped_before_the_alignment_tag(self) -> None:
        block = _block("Tom &amp; Jerry", settings="line:0%")
        block.subrip_alignment_conversion = True

        assert block.to_srt().payload == r"{\an8}Tom & Jerry"
