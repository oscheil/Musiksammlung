Ja. Es gibt inzwischen sehr gute Open-Source-Musikverwaltungen, die ähnlich wie **Immich** funktionieren: Du betreibst einen eigenen Server, verwaltest dort deine Musiksammlung und greifst über den Browser oder eine Smartphone-App darauf zu.

Allerdings gibt es bei Musik noch keine ganz so eindeutige Universallösung wie Immich bei Fotos.

Für eine private Musiksammlung auf einem Linux-Server würde ich vor allem **Navidrome, Jellyfin und Funkwhale** vergleichen.

## **Die interessantesten Lösungen**

[Friendship Ended with Spotify, now NIXOS is my Best Friend](https://images.openai.com/static-rsc-4/h_-UVSNc6jXKgPLR18-kX4ufbuT9JiVCjrvidzXtH8DXLrmmrOYHuNH4tqkU3Ko4-_sDJy1QNoaBRib7AYvbKMGxe0f3lY75b5Pqk8fCdVaDRG7pITeGkWWQujYk-JB9YHQIyjst6WI9VQf-wcH_Zf6_nv2azqQwYhCRPKD4BDc?purpose=inline)

**1. Navidrome – meine erste Wahl**

Schlanker Musikserver mit Albumcovern, Künstlern, Genres, Playlists, Suche, mehreren Benutzern und Smartphone-Apps. Auch für sehr große Sammlungen geeignet.

Navidrome

[Navidrome-Website](https://www.navidrome.org/?utm_source=chatgpt.com)

[I left Spotify. What happened next?](https://images.openai.com/static-rsc-4/hf9lwn6DiC5SfNUPRkWhHFVmPwOwXU1lEy9h8ZN9ZEWiKRPJ8LMgk_04Zli0lYvTOCvnmR7SKnKzjNbDlD1zxoeYr18KYZ7SE-2Jc1RMVsyr5FwUw_GOSB5dJ8PJvjG7bdq8vPSCP1dRMRK1oP6JBjGEj0flXAzo1TXPbymR_aE?purpose=inline)

**2. Jellyfin – für Musik und Videos**

Eine gemeinsame Medienverwaltung für Musik, Filme und Serien. Besonders interessant, wenn du ohnehin einen Medienserver betreibst. Die Musikverwaltung ist allerdings weniger spezialisiert als bei Navidrome.

[Jellyfin-Website](https://jellyfin.org/?utm_source=chatgpt.com)

[Funkwhale, un’alternativa Open Source a GrooveShark e Spotify, con l’implementazione del Fediverso \| by Funkcast & musicwhale \| Medium](https://images.openai.com/static-rsc-4/wwB8M9cOJUW8vjdK2OxftORZBF3TvnJT_iRwUZuPzcIDn9SB13denKcbd-IsN_aKWLZjfBDEVioY-ihcsvdwPovBl6XpiHU_vbi1B_YkPaLH3jmeFNxI0O-m5wQRZJpP82MWVSmqdengJ-TA6g1hANXZSKq0e4tIKgq37b7ResI?purpose=inline)

**3. Funkwhale – für gemeinsame Musiksammlungen**

Bietet Musikbibliotheken, Streaming und gemeinsame Nutzung. Interessant für mehrere Benutzer, aber komplexer zu betreiben.

[Funkwhale-Website](https://www.funkwhale.audio/?utm_source=chatgpt.com)

## **Vergleich mit Immich**

|                       |                   |               |               |
|-----------------------|-------------------|---------------|---------------|
| Eigenschaft           | Navidrome         | Jellyfin      | Funkwhale     |
| Eigener Linux-Server  | Ja                | Ja            | Ja            |
| Weboberfläche         | Ja                | Ja            | Ja            |
| Smartphone-Nutzung    | Sehr gut          | Gut           | Gut           |
| Albumcover            | Ja                | Ja            | Ja            |
| Metadatenverwaltung   | Vorwiegend lesend | Eingeschränkt | Eingeschränkt |
| Mehrere Benutzer      | Ja                | Ja            | Ja            |
| Ressourcenbedarf      | Gering            | Mittel        | Eher hoch     |
| Einfache Installation | Ja                | Ja            | Eher nein     |

## **Ein wichtiger Unterschied zu Immich**

Immich ist nicht nur ein Fotobetrachter, sondern auch ein leistungsfähiges Werkzeug zur Organisation einer Sammlung.

Bei Musik muss man zwei Aufgaben unterscheiden:

- **Musik abspielen und durchsuchen:** Dafür ist Navidrome hervorragend geeignet.
- **Musiksammlung pflegen:** Künstler, Albumtitel, Erscheinungsjahr, Genres, Cover und fehlerhafte Metadaten korrigieren. Dafür ist zusätzlich beispielsweise MusicBrainz Picard sinnvoll.

Navidrome verändert die Metadaten der Originaldateien normalerweise nicht, sondern liest sie ein. Das kann sogar ein Vorteil sein, wenn die Sammlung unverändert bleiben soll.

Für deine Linux-Umgebung wäre deshalb Navidrome ein guter erster Kandidat. Man könnte die Musikverzeichnisse zunächst ausschließlich lesend einbinden und die Verwaltung testen, ohne die Dateien zu verändern.

**Eine Frage ist für die Auswahl entscheidend:** Möchtest du hauptsächlich deine vorhandene Musiksammlung komfortabel **durchsuchen und abspielen**, oder möchtest du sie auch **systematisch organisieren, Metadaten korrigieren, Alben zuordnen und Dubletten finden** – also eher so, wie Immich eine Fotosammlung verwaltet?

-------------------------------

Ja, genau. **Die Dublettensuche muss nicht Bestandteil der Musikverwaltung sein.** Ich würde diese Aufgaben sogar bewusst trennen.

Für deine Musiksammlung wäre folgende Kombination sinnvoll:

- **Navidrome:** Zentrale Musikbibliothek mit Weboberfläche, Suche, Albumcovern, Playlists und Streaming im Heimnetz.
- **MusicBrainz Picard:** Korrektur und Ergänzung von Metadaten wie Künstler, Album, Titel, Erscheinungsjahr und Cover.
- **beets:** Optional für die systematische Organisation größerer Musiksammlungen, einschließlich Dublettenerkennung.
- **dupeGuru:** Für eine separate Suche nach doppelten oder ähnlichen Musikdateien.

Damit bleibt Navidrome schlank und die eigentlichen Musikdateien können zunächst unverändert bleiben.

Ein wesentlicher Unterschied zu Immich ist allerdings, dass **Navidrome seine Bibliothek hauptsächlich anhand der Metadaten in den Musikdateien aufbaut**. Gut gepflegte Tags sind daher wichtig.

Mich würde noch ein anderer Punkt interessieren: **Soll die Musikverwaltung ausschließlich Musikdateien verwalten, die bereits auf deinem Linux-Server liegen, oder möchtest du auch neue Musik über die Weboberfläche hochladen können?**

Das könnte die Wahl der Software beeinflussen.

---------------------------------------------------

Dann würde ich die Musikverwaltung etwas umfassender planen. **Navidrome bleibt ein guter Kandidat, aber allein reicht es für deine Vorstellungen nicht aus.**

Du möchtest im Grunde eine Musikverwaltung ähnlich Immich, die drei Aufgaben erfüllt:

1.  **Vorhandene Musik verwalten:** Künstler, Alben, Titel, Cover, Suche und Wiedergabe.
2.  **Neue Musik hinzufügen:** Beispielsweise aus YouTube oder durch Hochladen eigener Musikdateien.
3.  **Metadaten automatisch ergänzen:** Titel, Interpret, Album, Erscheinungsjahr, Genre und Cover aus Internetdatenbanken abrufen.

Ich würde diese Funktionen möglichst in getrennte Komponenten aufteilen. Dadurch bleibt die eigentliche Musikbibliothek unabhängig davon, woher neue Dateien kommen.

## **So könnte die Musikverwaltung aufgebaut sein**

**Neue Musik hinzufügen**

Datei-Upload im Browser · YouTube-Link · vorhandene Musikordner

**Importverzeichnis**

Neue Dateien zunächst getrennt von der Musiksammlung ablegen

**MusicBrainz Picard / AcoustID**

Musik erkennen · Metadaten und Cover abrufen · Ergebnisse kontrollieren

**Zentrale Musikbibliothek**

Dauerhafte, sauber organisierte Musikdateien

**Navidrome**

Weboberfläche · Suche · Wiedergabe · Playlists · Smartphone

## **Welche Programme übernehmen was?**

|                               |                        |
|-------------------------------|------------------------|
| Aufgabe                       | Software               |
| Musik verwalten und abspielen | Navidrome              |
| Musikdateien hochladen        | File Browser           |
| YouTube-Audio importieren     | yt-dlp                 |
| Titel automatisch erkennen    | AcoustID / Chromaprint |
| Metadaten und Cover ergänzen  | MusicBrainz Picard     |
| Dubletten separat untersuchen | beets oder dupeGuru    |

Navidrome unterstützt selbst keine Datei-Uploads und schreibt auch keine Metadaten in Musikdateien. Das ist ausdrücklich Teil seines Konzepts.

Navidrome+1

MusicBrainz Picard kann dagegen sogar Musikstücke anhand ihres akustischen Fingerabdrucks erkennen, wenn die Dateinamen wenig aussagekräftig sind.

MusicBrainz Picard v3.0 documentation+1

Für YouTube wäre yt-dlp ein mögliches Importwerkzeug. Das sollte nur für Inhalte verwendet werden, die du herunterladen darfst; außerdem sind die Nutzungsbedingungen der Plattform zu beachten.

## **Was ich zusätzlich sinnvoll fände**

Bei der Metadaten-Ergänzung würde ich nicht alles ungeprüft überschreiben lassen. Besser wäre eine Vorschau, die bisherige und vorgeschlagene Angaben gegenüberstellt. Anschließend kannst du die Änderungen übernehmen.

Eine solche Importoberfläche wäre eine kleine Ergänzung zu Navidrome und könnte im Heimnetz laufen.

**Eine wichtige Frage habe ich noch:** Möchtest du die Musik hauptsächlich als **vollständige Alben** verwalten, oder hast du viele **einzelne Musikstücke verschiedener Interpreten**, beispielsweise aus YouTube?

Das ist für die Auswahl der Metadatenverwaltung ziemlich entscheidend.

------------------------------------------------------------------------------------------------------

Dann würde ich die Musikverwaltung konsequent **titelorientiert statt albumorientiert** aufbauen.

Das vereinfacht die Anforderungen erheblich. Ein Album wäre lediglich eine Metadatenangabe zu einem Musikstück und müsste nicht als eigenständige Sammlung gepflegt werden.

## **So könnte die Verwaltung aussehen**

|                  |                                       |
|------------------|---------------------------------------|
| Feld             | Bedeutung                             |
| Titel            | Name des Musikstücks                  |
| Interpret        | Künstler oder Musikgruppe             |
| Album            | Optionaler Verweis auf ein Album      |
| Erscheinungsjahr | Jahr der Veröffentlichung             |
| Genre            | Rock, Klassik, Jazz usw.              |
| Komponist        | Optional                              |
| Cover            | Album- oder Titelbild                 |
| Quelle           | Beispielsweise eigene CD oder YouTube |
| Dateipfad        | Speicherort der Musikdatei            |

Eine Suche sollte über alle diese Angaben möglich sein. Außerdem wären eigene Tags und Playlists sinnvoll.

## **Welche Software passt dazu?**

**Navidrome** bleibt eine gute Möglichkeit, hat aber einen Nachteil: Seine Oberfläche ist stark auf Künstler und Alben ausgerichtet. Einzelne Titel lassen sich selbstverständlich suchen und abspielen, aber die Organisation folgt weitgehend den Metadaten der Dateien.

Eine interessante Alternative wäre **Ampache**.

Ampache bietet ebenfalls eine Weboberfläche, Musikstreaming, Künstler, Titel, Alben und Playlists. Außerdem besitzt es Funktionen zur Katalogverwaltung und Metadatenpflege. Es wäre deshalb einen Vergleich mit Navidrome wert.

[11 Best Free Spotify Alternatives in 2026](https://images.openai.com/static-rsc-4/TNxua-o1S7Mt442ujMhZDj-FgK9nI8_z0UUZWKDp0VLKo5j7fflGSYr8piuBBF0KgPlGqDGIKPbRN_CvGa0MoYutqFvK9FHk5dCXOVYAExE8g7AhnRsT7NNOo5Y9ucCm-YFIlKUAL4M4SBx6Tta6g2ChwajELldbbNOSIOzSm8A?purpose=inline)

Ampache

Umfangreichere Katalogverwaltung

[Vergeet Spotify en stream je eigen muziek met Navidrome \| ID.nl](https://images.openai.com/static-rsc-4/SvG0gRimW9I3fbbK8SZgafGayqr3cSQmc4w-SdCSwuOLL7JUHPmrvri8vxNBS86L_X7Ce5RRM4Z_0ik6hZUPzFojyvyqr-nTvm7mylMBisYe3Gw2uLFMsaR1jRZZFdtaD-uwjrc7xSj4kyR9oLpmQ8FXnlcrMpTbBS8f2VXjiTw?purpose=inline)

Navidrome

Schlankere Streaming-Oberfläche

Für deine Vorstellungen würde ich zunächst **Ampache und Navidrome praktisch vergleichen**, bevor wir uns festlegen.

Dabei würde ich besonders auf drei Dinge achten: eine gute Einzeltitelsuche, die automatische Ergänzung von Internet-Metadaten und einen einfachen Import neuer Musik.

Noch eine Frage, die für die Architektur wichtig ist:

**Möchtest du die Metadaten direkt in den Musikdateien speichern (ID3-Tags bei MP3 usw.), oder wäre dir eine zentrale Datenbank lieber, in der die Metadaten unabhängig von den Dateien verwaltet werden?**

Letzteres hätte den Vorteil, dass du zusätzliche Informationen, eigene Tags und Verknüpfungen speichern könntest, ohne die Musikdateien selbst verändern zu müssen.

-----------------------------------------------------

**Alle bisher genannten Programme sind Open Source und unter Linux nutzbar.** Die meisten lassen sich problemlos auf einem privaten Homeserver betreiben.

Allerdings unterscheiden sie sich deutlich: Einige sind vollständige Musikserver mit Weboberfläche, andere sind Werkzeuge für Import, Metadaten oder Dublettensuche.

## **1. Musikserver für deinen Homeserver**

|               |             |       |               |                  |
|---------------|-------------|-------|---------------|------------------|
| Software      | Open Source | Linux | Weboberfläche | Homeserver       |
| **Navidrome** | Ja          | Ja    | Ja            | Sehr gut         |
| **Ampache**   | Ja          | Ja    | Ja            | Sehr gut         |
| **Jellyfin**  | Ja          | Ja    | Ja            | Sehr gut         |
| **Funkwhale** | Ja          | Ja    | Ja            | Gut, aufwendiger |

Für deine Anforderungen würde ich **Navidrome und Ampache in die engere Auswahl nehmen**.

Navidrome ist besonders schlank und einfach zu betreiben. Ampache bietet eine umfangreichere Musikverwaltung, die für eine titelorientierte Sammlung interessant sein könnte.

## **2. Ergänzende Programme**

Auch diese Werkzeuge sind Open Source und Linux-tauglich:

|                    |                                |                   |
|--------------------|--------------------------------|-------------------|
| Programm           | Aufgabe                        | Serverbetrieb     |
| MusicBrainz Picard | Metadaten und Cover ergänzen   | Eher Desktop      |
| beets              | Automatische Musikorganisation | Ja, Kommandozeile |
| yt-dlp             | Erlaubte YouTube-Downloads     | Ja                |
| File Browser       | Dateien über Browser hochladen | Ja                |
| dupeGuru           | Dublettensuche                 | Eher Desktop      |

Die Programme müssen nicht alle dauerhaft laufen. Beispielsweise könnten beets und yt-dlp nur bei einem Import gestartet werden.

## **3. Meine Empfehlung für deinen Linux-Homeserver**

Ich würde mit **Ampache und Navidrome** beginnen und zunächst keine zusätzliche Eigenentwicklung vorsehen.

[11 Best Free Spotify Alternatives in 2026](https://images.openai.com/static-rsc-4/TNxua-o1S7Mt442ujMhZDj-FgK9nI8_z0UUZWKDp0VLKo5j7fflGSYr8piuBBF0KgPlGqDGIKPbRN_CvGa0MoYutqFvK9FHk5dCXOVYAExE8g7AhnRsT7NNOo5Y9ucCm-YFIlKUAL4M4SBx6Tta6g2ChwajELldbbNOSIOzSm8A?purpose=inline)

**Ampache**

Besonders interessant wegen der Katalogverwaltung. Läuft auf einem klassischen Webserver oder in Docker, ist unter AGPLv3 lizenziert.

ampache.org+1

[Website und Demo](https://ampache.org/?utm_source=chatgpt.com)

[Friendship Ended with Spotify, now NIXOS is my Best Friend](https://images.openai.com/static-rsc-4/h_-UVSNc6jXKgPLR18-kX4ufbuT9JiVCjrvidzXtH8DXLrmmrOYHuNH4tqkU3Ko4-_sDJy1QNoaBRib7AYvbKMGxe0f3lY75b5Pqk8fCdVaDRG7pITeGkWWQujYk-JB9YHQIyjst6WI9VQf-wcH_Zf6_nv2azqQwYhCRPKD4BDc?purpose=inline)

**Navidrome**

Besonders interessant wegen des geringen Ressourcenbedarfs. Läuft als Linux-Dienst ohne Docker, alternativ als Container. GPLv3.

Navidrome+1

[Website und Installation](https://www.navidrome.org/?utm_source=chatgpt.com)

Für deine Wünsche – Einzeltitel statt aufwendiger Albumverwaltung, Import neuer Musik und Ergänzung von Internet-Metadaten – würde ich **Ampache zuerst testen**. Ob es die gewünschte Metadatenpflege vollständig abdeckt, müssten wir praktisch prüfen.

Beide Programme können auf einem Debian- oder LMDE-Homeserver laufen. Deine Musikdateien könnten wir zunächst ausschließlich lesend einbinden, damit bei den Tests nichts verändert wird.

**Eine Frage zur Installation:** Möchtest du den Musikserver auf deinem bestehenden Linux-Rechner **terra11**, auf **terra-1240** oder auf einem anderen Rechner betreiben? Davon hängt ab, wie wir ihn am einfachsten installieren und ins Heimnetz integrieren.

---------------------------------------

Das ist eine wichtige zusätzliche Anforderung. Damit würde ich die Auswahl etwas anders gewichten.

Du möchtest im Grunde **eine zentrale Musikverwaltung auf terra-1240 und eine portable, auch offline nutzbare Musikverwaltung auf dem Fuji-Laptop**.

Dabei sollte nicht die gesamte Musiksammlung auf dem Laptop liegen müssen, sondern nur ein ausgewählter Teil.

Ich würde dafür folgende Architektur bevorzugen:

## **1. Zentrale und portable Musikbibliothek**

**terra-1240 – Hauptserver**

Vollständige Musiksammlung · Musikverwaltung · Metadaten · Weboberfläche

Synchronisation ausgewählter Musik

**Fuji-Laptop – portable Bibliothek**

Ausgewählte Titel lokal gespeichert · Offline-Suche · Offline-Wiedergabe

**Der entscheidende Punkt:** Die Musikdateien und ihre Metadaten sollten unabhängig von der jeweiligen Musikserver-Installation nutzbar sein.

Dann kannst du die Dateien auch mit anderen Musikprogrammen öffnen und bist nicht dauerhaft an Ampache oder Navidrome gebunden.

## **2. Welche Software eignet sich dafür?**

|                                         |           |                  |
|-----------------------------------------|-----------|------------------|
| Eigenschaft                             | Ampache   | Navidrome        |
| Zentraler Server auf terra-1240         | Ja        | Ja               |
| Zweite Installation auf Fuji            | Ja        | Ja               |
| Lokale Musik offline abspielen          | Ja        | Ja               |
| Ausgewählte Titel herunterladen         | Ja        | Ja               |
| Metadaten in Datenbank bearbeiten       | Ja        | Eingeschränkt    |
| Metadaten in Dateien zurückschreiben    | Optional  | Nein             |
| Kataloge von anderen Servern einbinden  | Ja        | Nicht direkt     |
| Synchronisation zwischen Installationen | Teilweise | Nicht integriert |

Ampache kann lokale und entfernte Kataloge verwalten. Die eigene Weboberfläche unterstützt allerdings keine vollständige Offline-Synchronisation; dafür sind zusätzliche Clients oder eine Dateisynchronisation nötig.

Ampache+1

Navidrome bietet zahlreiche kompatible Clients, teilweise mit Offline-Funktionen.

Navidrome

## **3. Meine Empfehlung**

Ich würde unter diesen Voraussetzungen **Ampache zunächst bevorzugen**, weil es eine flexiblere Katalog- und Metadatenverwaltung bietet.

Für den Fuji-Laptop sehe ich zwei Möglichkeiten:

**Variante A – eine zweite Ampache-Installation**

Auf terra-1240 liegt die vollständige Bibliothek. Auf Fuji läuft eine zweite Ampache-Instanz mit den lokal verfügbaren Titeln. Das wäre sinnvoll, wenn du auf beiden Rechnern möglichst dieselbe Weboberfläche haben möchtest.

**Variante B – Ampache auf terra-1240, lokaler Musikplayer auf Fuji**

Auf Fuji läuft beispielsweise Strawberry Music Player. Die ausgewählten Musikdateien werden lokal synchronisiert und lassen sich vollständig offline abspielen.

Variante B wäre deutlich einfacher und wartungsärmer. Allerdings hättest du auf Fuji nicht dieselbe Oberfläche wie auf dem Server.

## **4. Eine Entscheidung sollten wir noch treffen**

Für die portable Nutzung gibt es zwei unterschiedliche Anforderungen:

**Gleiche Musikverwaltung auf beiden Rechnern** – auch offline dieselbe Oberfläche, Suche und Metadatenverwaltung.

**Einfacher Offline-Zugriff auf Fuji** – ausgewählte Musik lokal abspielen und durchsuchen; die eigentliche Verwaltung erfolgt auf terra-1240.

Diese Variante weiterverfolgen

Die Antwort ist wichtig, weil wir damit entscheiden, ob auf Fuji ein zweiter Musikserver nötig ist oder ein wesentlich einfacherer Musikplayer ausreicht.

------------------------------------------------------------------------

# **Architektur für deine Musikverwaltung**

Ich würde die Lösung so aufbauen, dass **terra-1240 die zentrale Musikbibliothek verwaltet**, während der Fuji-Laptop eine ausgewählte Teilmenge lokal speichert und vollständig offline abspielen kann.

Dafür brauchen wir keine zweite Musikserver-Installation auf Fuji.

Meine bevorzugte Kombination wäre:

- **Ampache** auf terra-1240 als zentrale Musikverwaltung mit Weboberfläche.
- **Strawberry Music Player** auf Fuji für die lokale Wiedergabe und Suche.
- **Syncthing** für die Synchronisation ausgewählter Musikdateien.
- **MusicBrainz Picard und optional beets** für die Ergänzung und Pflege von Metadaten.
- **yt-dlp** als optionales Importwerkzeug für zulässige Downloads.

Alle Komponenten sind Open Source und Linux-tauglich.

## **1. Gesamtarchitektur**

**terra-1240 – Zentrale Musikverwaltung**

**Ampache – Weboberfläche**

Suche · Titel · Künstler · Playlists · Streaming

**Import und Metadatenpflege**

Upload · yt-dlp · MusicBrainz · beets

**Musikdateien – Hauptbibliothek**

Originaldateien · eingebettete Tags · Cover

**Syncthing**

Nur ausgewählte Titel · über Heimnetz

**Fuji – Portable Musikbibliothek**

**Lokale Musikdateien**

Ausgewählte Titel mit Metadaten und Covern

**Strawberry Music Player**

Offline-Suche · Wiedergabe · lokale Playlists

Das System funktioniert auch dann, wenn terra-1240 ausgeschaltet oder Fuji unterwegs ohne Netzwerkverbindung ist.

## **2. Die Verzeichnisstruktur**

Ich würde auf terra-1240 die folgenden logisch getrennten Verzeichnisse vorsehen. Die tatsächlichen Speicherpfade legen wir erst fest, wenn wir die vorhandenen Datenträger kennen.

*musik/*

*├── bibliothek/*

*│ ├── Rock/*

*│ ├── Jazz/*

*│ ├── Klassik/*

*│ └── ...*

*├── import/*

*│ ├── uploads/*

*│ └── youtube/*

*├── export-fuji/*

*└── backup/*

Die Genre-Unterverzeichnisse sind nur ein Beispiel. Da du einzelne Titel bevorzugst, würde ich **keine starre Album-Verzeichnisstruktur verlangen**. Die eigentliche Ordnung erfolgt über Metadaten und Suchfunktionen.

Wichtig ist die Trennung zwischen der Hauptbibliothek und dem Importbereich.

## **3. Metadaten: zentral pflegen, portabel erhalten**

Ich würde ein hybrides Modell verwenden:

**Standard-Metadaten direkt in den Musikdateien**, damit Fuji sie offline lesen kann. Dazu gehören Titel, Interpret, Album, Jahr, Genre und möglichst auch das Cover.

**Ergänzende Verwaltungsdaten in Ampache**, beispielsweise Bewertungen, Playlists und andere anwendungsspezifische Angaben.

Ampache unterstützt sowohl Datenbank-Metadaten als auch das Zurückschreiben in Dateien sowie Internetquellen wie MusicBrainz und TheAudioDB.

Ampache

Für die erste Phase würde ich das Zurückschreiben deaktivieren und zunächst nur prüfen, wie gut Ampache deine vorhandenen Titel erkennt.

## **4. Neue Musik importieren**

Ein interessanter Punkt: **Ampache besitzt bereits eine Upload-Funktion.** Dafür lässt sich ein eigener Upload-Katalog konfigurieren. Wir brauchen also möglicherweise gar keinen zusätzlichen File Browser.

Ampache

Der geplante Ablauf wäre:

1.  Musikdatei über die Weboberfläche hochladen oder eine zulässige YouTube-Datei mit yt-dlp importieren.
2.  Neue Datei zunächst im Importbereich speichern.
3.  Metadaten und Cover über MusicBrainz ergänzen und kontrollieren.
4.  Erst nach Freigabe in die eigentliche Musikbibliothek übernehmen.
5.  Ampache aktualisiert anschließend seinen Katalog.

Damit verhindern wir, dass fehlerhafte Metadaten oder unpassende Downloads unmittelbar in der Hauptsammlung landen.

## **5. Wie kommen ausgewählte Titel auf Fuji?**

Hier würde ich zunächst **Syncthing mit einem separaten Exportverzeichnis** verwenden.

terra-1240

Send Only

*musik/export-fuji/*

Synchronisation im Heimnetz

*~/Musik/Offline/*

Fuji-Laptop

Receive Only

Diese Betriebsarten unterstützt Syncthing ausdrücklich.

Syncthing documentation

Allerdings ist ein wichtiger Punkt zu beachten: Syncthing synchronisiert **Verzeichnisse, nicht automatisch eine Titelauswahl aus Ampache**.

Für die erste Version würde ich deshalb Titel gezielt in das Exportverzeichnis kopieren. Später könnten wir eine Ampache-Playlist als Grundlage für die Auswahl verwenden.

Änderungen und Löschungen im Exportverzeichnis können sich auf Fuji auswirken. Die Hauptbibliothek bleibt davon getrennt. Auf Fuji sollten die synchronisierten Dateien möglichst nicht direkt bearbeitet werden.

## **6. Strawberry auf Fuji**

[Der Clementine Player ist tot, es lebe der Strawberry Music Player - Natenoms Blog](https://images.openai.com/static-rsc-4/w49vMcsjV_2coUxbFwjz-b5JZVfJ7lWOMeV37MWRyDhNrzd9D3Lm9Nt2REurw7muLljXvLVf3PuaQtediKoaCy2Fi_L7Mjg9Rk3aXZp9-EEjntp1Y5v6e0GKx3XRFHFejcPw1b7jlt3a6rca8bGSMJkZMmr2hSKg8UhybVF-nfE?purpose=inline)

Strawberry Music Player

Strawberry bietet eine lokale Musikbibliothek, Titelsuche, Playlists, Tag-Bearbeitung, MusicBrainz-Anbindung und zahlreiche Audioformate. Es kann außerdem mit Subsonic-kompatiblen Servern kommunizieren.

strawberrymusicplayer.org

[Projektwebsite](https://strawberrymusicplayer.org/?utm_source=chatgpt.com)

Damit könntest du auf Fuji sowohl die lokal gespeicherten Titel offline abspielen als auch bei bestehender Netzwerkverbindung auf die zentrale Sammlung zugreifen, sofern die Serveranbindung passend eingerichtet ist.

## **7. Umsetzung in überschaubaren Schritten**

Ich würde das Projekt nicht sofort vollständig installieren, sondern in vier Phasen aufteilen.

**Phase 1 – Bestandsaufnahme**

Auf terra-1240 vorhandene Musikverzeichnisse, Dateiformate, Speicherplatz und bestehende Webserver prüfen. Ausschließlich lesend.

**Phase 2 – Ampache testen**

Kleine Testbibliothek einlesen, Einzeltitelsuche, Cover, Metadaten, Upload und Streaming prüfen. Originaldateien unverändert lassen.

**Phase 3 – Fuji anbinden**

Strawberry installieren, kleine Musikauswahl übertragen und Offline-Betrieb testen. Danach Syncthing einrichten.

**Phase 4 – Import automatisieren**

MusicBrainz, YouTube-Import, Metadatenvorschau und Auswahl für Fuji ergänzen.

## **8. Eine Architekturentscheidung würde ich noch offenlassen**

Bei der Installation von Ampache auf terra-1240 gibt es zwei sinnvolle Möglichkeiten:

|                            |                                   |                                   |
|----------------------------|-----------------------------------|-----------------------------------|
|                            | Native Installation               | Docker                            |
| Integration in Linux       | Direkt                            | Isolierter Container              |
| Abhängigkeiten             | PHP, Webserver, Datenbank         | Über Container verwaltet          |
| Updates                    | Paket-/Anwendungsverwaltung       | Container-Updates                 |
| Sicherung                  | Dateien, Konfiguration, Datenbank | Volumes, Konfiguration, Datenbank |
| Parallelbetrieb zum Testen | Möglich                           | Besonders praktisch               |

Ich würde **Docker nicht automatisch voraussetzen**. Eine native Installation kann auf deinem Linux-Server ebenso sinnvoll sein.

**Mein Vorschlag für den nächsten Schritt:** Wir beginnen mit einer rein lesenden Bestandsaufnahme von terra-1240 und prüfen, welche Voraussetzungen bereits vorhanden sind. Erst danach entscheiden wir über die Installationsart.

Dabei können wir wie bei deinen anderen Linux-Projekten mit wenigen gezielten Terminalbefehlen arbeiten, längere Ausgaben in Dateien speichern und vor Änderungen Sicherungen anlegen.

---------------------------------------------------------------------------------------------

Für deine Musiksammlung würde ich die Softwareauswahl jetzt etwas anders gewichten als ursprünglich.

**Entscheidend ist nicht nur, dass ein Musikserver neue Dateien einlesen kann. Er sollte auch mit mehreren Sammlungen, unterschiedlichen Dateiformaten und möglichen Dubletten umgehen können.**

Dabei muss man zwei Funktionen unterscheiden:

- **Musikverwaltung:** Titel suchen, abspielen, Metadaten bearbeiten, neue Verzeichnisse einlesen.
- **Dublettenverwaltung:** Identische Dateien erkennen, verschiedene Versionen eines Musikstücks vergleichen und entscheiden, welche erhalten bleiben.

Nur wenige Programme beherrschen beides wirklich gut.

## **Die interessantesten Programme**

|                        |                                    |                                       |                                                |
|------------------------|------------------------------------|---------------------------------------|------------------------------------------------|
| Software               | Neue Sammlungen                    | Dublettenbehandlung                   | Einschätzung                                   |
| **Ampache**            | Gut, mehrere Kataloge              | Eingeschränkt                         | Gute zentrale Webverwaltung                    |
| **Navidrome**          | Gut, automatische Bibliotheksscans | Eingeschränkt                         | Besonders gut für Streaming                    |
| **beets**              | Sehr gut, kontrollierter Import    | Gut, über Metadaten und Erweiterungen | Besonders interessant für deine Sammlung       |
| **MusicBrainz Picard** | Gut, auch stapelweise              | Eingeschränkt                         | Sehr gut für Metadaten und Identifizierung     |
| **Lidarr**             | Automatisierte Musikbibliothek     | Teilweise, über Qualitätsprofile      | Eher albumorientiert, für dich weniger passend |

Für deine überwiegend **titelorientierte** Sammlung würde ich vor allem **Ampache und beets** näher betrachten.

Ampache wäre die zentrale Oberfläche, während beets neue Musik prüft, Metadaten ergänzt und mögliche Dubletten erkennt, bevor sie in die Bibliothek übernommen wird.

Wichtig ist dabei: beets ist primär ein Kommandozeilenwerkzeug, keine vollständige browserbasierte Musikverwaltung. Und weder Ampache noch Navidrome sind vollwertige Werkzeuge zur zuverlässigen Bereinigung aller Dublettenarten.

## **Deine Prüfsummendatei liefert bereits ein klares Ergebnis**

Ich habe die hochgeladene SHA-256-Datei ausgewertet.

Geprüfte Audiodateien

# **17.123**

Unterschiedliche Dateiinhalte

# **10.604**

Dublettengruppen

# **6.279**

Überzählige identische Kopien

# **6.519**

Das ist eine erhebliche Überschneidung: Rund **38 % der geprüften Audiodateien sind zusätzliche, bytegenau identische Kopien**.

Dabei sind noch keine Musikstücke berücksichtigt, die beispielsweise einmal als MP3 und einmal als OGG vorliegen.

## **Meine Empfehlung für terra-1240**

Ich würde die Architektur folgendermaßen aufbauen:

**Neue Musiksammlungen**

USB-Laufwerk, Uploads, weitere Rechner

**beets + Prüfsummenvergleich**

Metadaten, Dublettenkandidaten, kontrollierter Import

**Zentrale Musikbibliothek + Ampache**

Suche, Wiedergabe, Playlists, Weboberfläche

**Fuji-Laptop**

Ausgewählte Musik offline mit Strawberry

**Ich würde jetzt noch keine Musikdateien zusammenführen oder löschen.** Zunächst sollten wir die 6.279 Dublettengruppen genauer auswerten, insbesondere welche Verzeichnisse sich überschneiden.

Danach können wir entscheiden, ob Ampache direkt alle drei Verzeichnisse einliest oder ob wir langfristig eine bereinigte zentrale Musikbibliothek aufbauen.

Letzteres halte ich angesichts der Ergebnisse für die bessere Lösung.

--------------------------------------------------------------------

Das ist ein wichtiger zusätzlicher Punkt. **Unsere Musikverwaltung muss auch mit unvollständigen oder völlig fehlenden Metadaten sinnvoll funktionieren.** Gerade bei Radioaufnahmen dürfen wir nicht voraussetzen, dass Künstler, Titel oder Album bekannt sind.

Ich würde deshalb die bisherige Planung etwas erweitern.

## **Zwei Arten von Musikaufnahmen**

|                    |                          |                                        |
|--------------------|--------------------------|----------------------------------------|
| Eigenschaft        | Einzelne Musiktitel      | Radioaufnahmen                         |
| Künstler           | Meist bekannt            | Oft unbekannt                          |
| Titel              | Meist bekannt            | Manchmal nur Sendungsname              |
| Album              | Optional                 | Häufig nicht vorhanden                 |
| Sender             | Normalerweise irrelevant | Wichtig                                |
| Aufnahmedatum      | Optional                 | Wichtig, soweit bekannt                |
| Dauer              | Meist wenige Minuten     | Auch mehrere Stunden                   |
| Inhalt             | Ein Musikstück           | Mehrere Stücke, Moderation, Interviews |
| Metadatenerkennung | MusicBrainz/Picard       | Oft nur eingeschränkt möglich          |

Eine zweistündige Radiosendung sollte beispielsweise **als eine eigenständige Aufnahme erhalten bleiben**, auch wenn darin zwanzig Musikstücke vorkommen.

## **Was das für unsere Architektur bedeutet**

Ich würde eine gemeinsame Bibliothek mit unterschiedlichen Eintragstypen vorsehen:

- **Musiktitel:** Einzelne Stücke mit Künstler, Titel, optionalem Album und weiteren Metadaten.
- **Radiosendung:** Eine vollständige Aufnahme mit Sender, Sendungsname, Datum, Beschreibung und gegebenenfalls einer Titelliste.
- **Unbekannte Aufnahme:** Eine Datei, die noch nicht identifiziert wurde, aber trotzdem sofort gesucht und abgespielt werden kann.

Diese Unterscheidung würde ich in unserer Importverwaltung vorsehen. Wir müssen noch prüfen, wie gut Ampache die zusätzlichen Felder abbilden kann; möglicherweise benötigen wir dafür ergänzende Metadaten in unserer eigenen Datenbank.

## **Dubletten bei Radioaufnahmen**

Hier müssen wir besonders vorsichtig sein.

Eine Radiosendung könnte beispielsweise zweimal vorhanden sein, einmal als MP3 und einmal als OGG. Oder eine Aufnahme enthält nur einen Ausschnitt einer längeren Sendung.

Deshalb würde ich drei Erkennungsstufen vorsehen:

|       |                                                                     |                                     |
|-------|---------------------------------------------------------------------|-------------------------------------|
| Stufe | Verfahren                                                           | Konsequenz                          |
| 1     | Identische SHA-256-Prüfsumme                                        | Sicher identische Datei             |
| 2     | Gleiche oder ähnliche Metadaten, Dauer und technische Eigenschaften | Dublettenkandidat                   |
| 3     | Audio-Fingerprinting, gegebenenfalls akustischer Vergleich          | Möglicherweise gleicher Audioinhalt |

Insbesondere bei Radiosendungen dürfen wir nicht allein aufgrund ähnlicher Titel oder gleicher Sendedaten automatisch Dateien entfernen.

## **Meine Empfehlung**

Für terra-1240 würde ich jetzt eine **dauerhafte, format- und metadatenunabhängige Musik-Importverwaltung** vorsehen.

Die Kombination könnte weiterhin aus Ampache für die Weboberfläche und beets/Picard für die Metadatenbearbeitung bestehen. Eine kleine SQLite-Datenbank würde zusätzlich die Herkunft, Prüfsummen, Importentscheidungen und Radio-spezifischen Informationen verwalten.

Damit könnten wir später auch große neue Sammlungen importieren, ohne bereits vorhandene Dateien erneut aufnehmen zu müssen. Unbekannte Aufnahmen würden nicht abgewiesen, sondern zunächst mit ihren vorhandenen Dateiinformationen katalogisiert.

**Eine Frage ist dafür noch entscheidend:**

Enthalten deine künftigen Radioaufnahmen überwiegend **vollständige Sendungen von beispielsweise 30 bis 180 Minuten**, oder sind es eher **einzelne Musikstücke, die aus Radiosendungen aufgenommen wurden**?

Beides können wir unterstützen, aber die passende Metadaten- und Dublettenstrategie unterscheidet sich deutlich.

----------------------------------------------------------------------------------

Dann wird die Planung deutlich einfacher. **Wir bleiben bei einer titelorientierten Musikverwaltung.** Radioaufnahmen behandeln wir grundsätzlich wie normale Musikstücke, auch wenn Metadaten fehlen.

Längere Radiosendungen können als Sonderfall ebenfalls aufgenommen werden, benötigen aber keine eigene Verwaltungssoftware.

Für unsere zentrale Musikbibliothek auf terra-1240 würde ich folgende Regeln festlegen:

- **Album ist optional.** Auch Künstler und Titel dürfen zunächst unbekannt sein.
- **Jede Audiodatei erhält einen eigenen Eintrag**, zunächst gegebenenfalls nur anhand ihres Dateinamens.
- **Metadaten können später ergänzt werden**, manuell oder mithilfe von MusicBrainz und Audio-Fingerprinting.
- **Neue Sammlungen werden zuerst auf Dubletten geprüft**, bevor neue Dateien in die zentrale Bibliothek gelangen.
- **Unterschiedliche Aufnahmen und Versionen bleiben erhalten**, solange nicht zuverlässig feststeht, dass sie redundant sind.
- **Die Herkunft bleibt dokumentiert**, damit wir später nachvollziehen können, aus welcher Sammlung eine Aufnahme stammt.

Damit passt die Kombination aus Ampache, einer kontrollierten Importverwaltung und ergänzenden Werkzeugen zur Metadatenerkennung weiterhin gut.

### **Wie wir jetzt weitermachen**

Ich würde zunächst die bereits erkannten bytegenauen Dubletten bereinigen – genauer gesagt: eine neue Bibliothek erzeugen, in der jede identische Datei nur einmal vorkommt.

Die drei ursprünglichen Sammlungen bleiben unverändert. Das ist besonders wichtig, solange wir die neue Verwaltung noch erproben.

**Eine Frage zur Auswahl der Dateien:** Wenn ein Musikstück mehrfach mit exakt identischem Dateiinhalt vorhanden ist, spielt es für dich eine Rolle, aus welchem der drei Verzeichnisse wir die Kopie übernehmen? Oder können wir einfach eine beliebige identische Kopie auswählen?

Bei identischem Dateiinhalt gibt es keinen Qualitätsunterschied. Die Entscheidung betrifft lediglich den ursprünglichen Dateipfad und die spätere Nachvollziehbarkeit.

-------------------------------------------------------------------------------------------------------

Das sollten wir unbedingt berücksichtigen. **Der Speicherort einer Musikdatei darf nicht ihre Identität bestimmen.**

Damit können wir später Musikdateien zwischen Verzeichnissen oder Festplatten verschieben, ohne dass die Musikverwaltung sie automatisch als neue Titel behandelt oder ihre Metadaten verliert.

## **So würde ich das lösen**

Wir unterscheiden drei Dinge:

|                  |                                                                 |
|------------------|-----------------------------------------------------------------|
| Bestandteil      | Aufgabe                                                         |
| **Musikeintrag** | Dauerhafte interne ID, Titel, Künstler, Beschreibung, Tags      |
| **Audiodatei**   | Dateiformat, Größe, SHA-256-Prüfsumme, technische Eigenschaften |
| **Speicherort**  | Aktueller Dateipfad und Datenträger                             |

Ein Musikeintrag kann mit mehreren Audiodateien verknüpft sein, beispielsweise einer MP3- und einer FLAC-Version. Dieselbe Audiodatei kann außerdem an mehreren Speicherorten vorkommen.

### **Beispiel**

**Musikeintrag 10482**

Titel: Unbekannt · Künstler: Unbekannt

**Audiodatei**

SHA-256: a83f… · MP3

Alter Speicherort

/mnt/datensichv/von_media/Musik/...

Früher

Neuer Speicherort

/mnt/datensichv/Musikbibliothek/...

Aktuell

Bei einem erneuten Scan erkennt unsere Importverwaltung anhand der Prüfsumme die Datei am neuen Speicherort und aktualisiert die Zuordnung. Die Metadaten bleiben mit der dauerhaften ID verbunden.

Dabei gibt es eine wichtige Unterscheidung: **Unsere eigene Importdatenbank kann das so verwalten.** Ob Ampache selbst beim Verschieben einer Datei alle internen Informationen, etwa Playlist-Zuordnungen, erhält, müssen wir gesondert prüfen. Deshalb sollten Pfadänderungen später kontrolliert mit Ampache synchronisiert werden.

## **Konsequenz für die Dublettenbereinigung**

Für die bereits gefundenen identischen Kopien können wir eine beliebige auswählen. Wir speichern aber auch die ursprünglichen Fundorte.

Ich würde folgende Reihenfolge wählen:

1.  Die drei vorhandenen Sammlungen in eine SQLite-Bestandsdatenbank aufnehmen.
2.  Die vorhandenen SHA-256-Prüfsummen importieren und identische Dateien zuordnen.
3.  Einen Plan für die neue, dublettenbereinigte Bibliothek erstellen.
4.  Den Plan prüfen und erst anschließend die ausgewählten Dateien kopieren.
5.  Später neue Sammlungen über denselben Mechanismus einlesen.

So müssen wir bei zukünftigen größeren Importen nicht wieder bei null anfangen. Unveränderte Dateien können anhand ihrer gespeicherten Eigenschaften wiedererkannt werden; nur neue oder unklare Dateien benötigen zusätzliche Prüfungen.

**Mein Vorschlag für den nächsten praktischen Schritt:** Wir erstellen zunächst die SQLite-Bestandsdatenbank aus der vorhandenen Prüfsummendatei. Noch keine Musikdateien kopieren, verschieben oder löschen.

Damit schaffen wir eine dauerhafte Grundlage sowohl für die Dublettenbereinigung als auch für spätere Erweiterungen.
