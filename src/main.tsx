import { Plugin } from "obsidian";
import { createRoot, Root } from "react-dom/client";
import { StrictMode } from "react";
import React from "react";
import FloatingWidget from "./FloatingWidget";
import { AIPluginSettings, DEFAULT_SETTINGS, AISettingTab } from "./settings";

export default class AIPlugin extends Plugin {
  private root: Root | null = null;
  private container: HTMLElement | null = null;
  settings: AIPluginSettings = DEFAULT_SETTINGS;

  async onload() {
    // Create a div and append to document.body
    await this.loadSettings();
    this.addSettingTab(new AISettingTab(this.app, this));
    this.container = document.createElement("div");
    this.container.id = "my-plugin-root";
    document.body.appendChild(this.container);

    // Mount React into it
    this.root = createRoot(this.container);
    this.root.render(
      <StrictMode>
        <FloatingWidget />
      </StrictMode>,
    );
  }

  onunload() {
    // Clean up on plugin disable
    this.root?.unmount();
    this.container?.remove();
  }

  async loadSettings() {
    this.settings = Object.assign(
      {},
      DEFAULT_SETTINGS,
      (await this.loadData()) as Partial<AIPluginSettings>,
    );
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }
}
