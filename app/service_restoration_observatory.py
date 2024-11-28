import altair
import pandas
import streamlit


PERCENTILE = "percentile"
DECILE = "decile"
MEDIAN = "median"

systolic_bp_url = "https://jobs.opensafely.org/service-restoration-observatory/sro-key-measures-dashboard/published/01GGZ1273Y8PM2QYPWBDXWT433/"
systolic_bp = pandas.read_csv(systolic_bp_url, parse_dates=["date"])
systolic_bp["type"] = PERCENTILE
systolic_bp.loc[systolic_bp.percentile % 10 == 0, "type"] = DECILE
systolic_bp.loc[systolic_bp.percentile == 50, "type"] = MEDIAN

streamlit.title("Service Restoration Observatory")

streamlit.header("Blood Pressure Monitoring")

streamlit.markdown("""
    The codes used for this measure are available in [this codelist][1].

    [1]: https://www.opencodelists.org/codelist/opensafely/systolic-blood-pressure-qof/3572b5fb/
""")

with streamlit.expander("What is it and why does it matter?"):
    streamlit.markdown("""
        A commonly-used assessment used to identify patients with hypertension or
        to ensure optimal treatment for those with known hypertension.
        This helps ensure appropriate treatment,
        with the aim of reducing long term risks of complications from hypertension
        such as stroke, myocardial infarction, and kidney disease.
    """)

with streamlit.expander("Caveats"):
    streamlit.markdown("""
        We use codes which represent results reported to GPs,
        so tests requested but not yet reported are not included.
        Only test results returned to GPs are included,
        which will usually exclude tests requested while a person is in hospital and
        other settings like a private clinic.
    """)


streamlit.altair_chart(
    altair.Chart(systolic_bp)
    .mark_line()
    .encode(
        x=altair.X("date", title=None),
        y=altair.Y("value", title="Rate per 1000 registered patients"),
        detail=PERCENTILE,
        strokeDash=altair.StrokeDash(
            "type",
            title=None,
            scale=altair.Scale(
                domain=[PERCENTILE, DECILE, MEDIAN],
                range=[[1, 1], [4, 2], [0]],
            ),
        ),
        strokeWidth=altair.condition(
            altair.datum.type == MEDIAN, altair.value(1), altair.value(0.5)
        ),
    ),
    use_container_width=True,
)
