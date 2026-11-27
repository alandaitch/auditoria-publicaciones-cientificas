# How Let’s Fix Science assigns papers

We select consequential, testable claims among 50,000 highly cited scientific papers.
The first question is practical. What published conclusion could an independent check change?
A reproducible match is as valuable as a discrepancy. Both can settle the question.

## The population

The frozen [OpenAlex query](https://api.openalex.org/works?filter=to_publication_date%3A2025-12-31%2Ctype%3Aarticle%7Creview%2Cis_retracted%3Afalse%2Cprimary_location.source.type%3Ajournal%7Cconference&sort=cited_by_count%3Adesc) uses the 2026-11-27 UTC snapshot.
We selected articles and reviews published through 2025 from journals or conference sources.
OpenAlex records marked retracted at collection were excluded.
We ranked distinct OpenAlex work IDs by citations, breaking ties by numeric ID.
Some editions may have separate IDs. Duplicate DOIs are deferred for new assignments.
The cutoff was **1,767 citations**. The group received **192,125,824 citations** altogether.
A citation can reference any claim in a paper.
Bibliographic classifications and citation coverage depend on OpenAlex.

[All 50,000 records, in citation order](bibliography.csv) · [Public progress](mission.json)

## Assignment order

Rules screen the available abstracts for testable claims. OpenAlex fields organize disciplinary coverage.
It looks for numerical comparisons, pooled estimates, mathematical guarantees and testable coverage claims.
The screen favors consequential outcomes and a concrete test with published evidence.
Reported data or code availability is a clue. Reviewers must verify availability themselves.
It assigns **828** priority and **4,485** possible opportunities.
**26,278** have few detectable signals. **18,409** lack enough usable text.
The first version recognizes English-language patterns. Short or missing abstracts require another source.
These categories guide reading. No category estimates the probability that a paper is wrong.
Submissions are private. Volunteers receive the assigned paper without the internal score.

While all categories have eligible papers, ten consecutive positions include five priority opportunities,
three possible opportunities, one low-signal paper and one paper with insufficient information.
Domains and fields alternate within categories. Selected fields, prior checks and active reservations affect actual assignments.
As categories empty, the service continues with the remaining papers.
Two Terra agents independently evaluated 30 summaries without seeing scores or citation counts.
They agreed on 28 of 30 reading priorities. This measured agreement about auditability.
Confirmed consequential findings per review hour can assess the strategy after actual checks.

## Reading progress

We have documented checks on **60** papers in this population.
**53** contribute in aggregate only.
**0** have a published independent verification.
Each paper counts once, irrespective of the number or outcome of tests.
Waiting for the author requires a verified notice and a thread check.
Unreleased results only contribute to aggregate counts. Private correspondence stays private.
Historical records and existing reservations remain available through the original workflow.
**899** papers from the original thousand belong to this population.
Older work outside the new cutoff remains archived and counts separately.

## En español

Elegimos qué afirmaciones revisar entre 50.000 trabajos muy citados.
Buscamos conclusiones importantes que puedan contrastarse con datos, comparaciones o demostraciones.
La selección usa artículos y revisiones publicados hasta 2025 según OpenAlex.
El corte fue de **1.767 citas**. La población suma **192.125.824 citas**.
El orden de lectura combina oportunidades prioritarias, posibles y artículos con poca información.
También reservamos turnos para trabajos que pueden escapar al filtro automático.
Los resúmenes breves, ausentes o en otros idiomas requieren consultar otra fuente.
Cada aporte se verifica antes de publicar cualquier resultado identificable.
Las citas indican cuánto se cita un trabajo. Cada prueba examina una afirmación concreta.

[Contribute / Participá](CONTRIBUTING.md)
