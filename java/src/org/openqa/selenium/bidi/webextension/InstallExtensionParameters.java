package org.openqa.selenium.bidi.webextension;


public class InstallExtensionParameters {

  private final ExtensionData extensionData;

  public InstallExtensionParameters(ExtensionData extensionData) {
    this.extensionData = extensionData;
  }

  public ExtensionData getExtensionData() {
    return extensionData;
  }
}
