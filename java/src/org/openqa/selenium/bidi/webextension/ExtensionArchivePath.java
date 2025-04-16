package org.openqa.selenium.bidi.webextension;

import java.util.Map;

public class ExtensionArchivePath extends ExtensionData {
  private final String path;

  public ExtensionArchivePath(String path) {
    this.path = path;
  }

  @Override
  public Map<String, Object> toMap() {
    String type = "archivePath";
    return Map.of("extensionData", Map.of("type", type, "path", path));
  }
}
