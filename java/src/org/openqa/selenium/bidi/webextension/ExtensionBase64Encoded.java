package org.openqa.selenium.bidi.webextension;

import java.util.Map;

public class ExtensionBase64Encoded extends ExtensionData {
  private final String path;

  public ExtensionBase64Encoded(String path) {
    this.path = path;
  }

  @Override
  public Map<String, Object> toMap() {
    String type = "base64";
    return Map.of("extensionData", Map.of("type", type, "path", path));
  }
}
