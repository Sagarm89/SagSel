package org.openqa.selenium.bidi.webextension;

import java.util.Map;

public class UninstallExtensionParameters {

  public final Map<String, Object> extension;

  public UninstallExtensionParameters(Map<String, Object> extension) {
    this.extension = extension;
  }


}
