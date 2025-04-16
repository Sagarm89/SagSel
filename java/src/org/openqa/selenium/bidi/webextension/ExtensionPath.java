package org.openqa.selenium.bidi.webextension;

import java.util.Map;

public class ExtensionPath extends ExtensionData {
  private final String path;

  public ExtensionPath(String path) {
    this.path = path;
  }

  @Override
  public Map<String, Object> toMap() {
    String type = "path";
    return Map.of("extensionData", Map.of("type", type, "path", path));
  }
}
