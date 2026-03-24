import { App, PluginSettingTab, Setting } from "obsidian";
import AIPlugin from "./main";

export interface AIPluginSettings {
	mySetting: string;
}

export const DEFAULT_SETTINGS: AIPluginSettings = {
	mySetting: "default",
};

export class AISettingTab extends PluginSettingTab {
	plugin: AIPlugin;

	constructor(app: App, plugin: AIPlugin) {
		super(app, plugin);
		this.plugin = plugin;
	}

	display(): void {
		const { containerEl } = this;

		containerEl.empty();

		new Setting(containerEl)
			.setName("Settings #1")
			.setDesc("It's a secret")
			.addText((text) =>
				text
					.setPlaceholder("Enter your secret")
					.setValue(this.plugin.settings.mySetting)
					.onChange(async (value) => {
						this.plugin.settings.mySetting = value;
						await this.plugin.saveSettings();
					}),
			);
	}
}
