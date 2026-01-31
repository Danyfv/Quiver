# 🏹 Quiver

**Quiver** è un launcher "super ottimizzato" e rapidissimo per Windows, progettato per la massima efficienza. Ti permette di eseguire script, avviare programmi e incollare testi dinamici tramite una combinazione di tasti globale.

![Quiver Icon](quiver/resources/icon_green.png)

## ✨ Funzionalità Principali

*   **🚀 Velocità Estrema**: Interfaccia minimalista in PyQt6 che appare istantaneamente.
*   **⌨️ Keyboard-First**: Attiva il launcher ovunque con una hotkey (default `Alt+Q`).
*   **🛠️ Esecuzione Versatile**:
    *   Avvia script **Python**.
    *   Esegui file **Batch (.bat)**.
    *   Lancia **Programmi (.exe)**.
    *   Inserisce **Testo** predefinito.
*   **🔄 Output Dinamico & Replace**: I comandi possono restituire output che viene processato per sostituire tag dinamici (es. `<<DATA>>` diventa `23/11/2025`).
*   **🗂️ Menu Nidificati**: Organizza i tuoi strumenti in sottomenu navigabili.
*   **🎨 Feedback Visivo**: L'icona nella System Tray cambia colore in base allo stato:
    *   🟢 **Verde**: Pronto (Idle)
    *   🔵 **Blu**: In esecuzione (Running)
    *   🔴 **Rosso**: Errore (Error)
*   **👻 Stealth & Trasparente**: Finestra semi-trasparente e senza bordi che non disturba il workflow.

---

## 📦 Installazione

Quiver utilizza `uv` per una gestione rapida e moderna delle dipendenze Python.

1.  **Installa UV** (se non lo hai già):
    ```bash
    pip install uv
    ```

2.  **Installa le dipendenze**:
    Nella cartella del progetto, esegui:
    ```bash
    uv sync
    # oppure
    uv pip install -r requirements.txt
    ```

3.  **Avvia Quiver**:
    ```bash
    python -m uv run main.py
    ```

---

## ⚙️ Configurazione

Quiver è completamente configurabile tramite file JSON.

### 1. Configurazione Generale (`config.json`)
Modifica questo file per cambiare la combinazione di tasti globale.
```json
{
    "hotkey": "alt+q"
}
```

### 2. Menu Comandi (`menus/default.json`)
Qui definisci le azioni disponibili nel launcher. Puoi creare altri file JSON in questa cartella per menu aggiuntivi (navigabili via Tab).

**Tipi di comandi supportati:**

*   **`program`**: Avvia un eseguibile.
*   **`bat`**: Esegue uno script batch.
*   **`python`**: Esegue uno script Python.
*   **`text`**: Restituisce un testo statico (utile per snippet).
*   **`menu`**: Crea un sottomenu.

**Esempio:**
```json
[
    {
        "label": "Blocco Note",
        "type": "program",
        "command": "notepad.exe"
    },
    {
        "label": "Mio Script",
        "type": "python",
        "command": "scripts/mio_script.py"
    },
    {
        "label": "Firma Email",
        "type": "text",
        "content": "Cordiali saluti,\nMario Rossi"
    },
    {
        "label": "Strumenti Avanzati",
        "type": "menu",
        "items": [
            { "label": "Tool 1", "type": "bat", "command": "tool1.bat" }
        ]
    }
]
```

### 3. Sostituzione Dinamica (`replace.json`)
Definisci dei "tag" che, se presenti nell'output di un comando o in un testo, vengono sostituiti automaticamente eseguendo un altro script.

**Esempio:**
Se hai un comando testo che restituisce: `"Oggi è il <<DATA>>"`.
E configuri `replace.json` così:
```json
{
    "<<DATA>>": {
        "type": "python",
        "command": "scripts/get_date.py"
    }
}
```
Quiver eseguirà `get_date.py` e sostituirà `<<DATA>>` con il risultato.

---

## 🖥️ Utilizzo

1.  Premi `Alt+Q` (o la tua hotkey personalizzata).
2.  Digita per filtrare i comandi.
3.  Premi `Invio` o clicca per eseguire.
4.  L'output (se presente) viene copiato automaticamente negli appunti.
5.  Premi `Esc` per chiudere la finestra senza eseguire nulla.
