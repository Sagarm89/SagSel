// Licensed to the Software Freedom Conservancy (SFC) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The SFC licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

package org.openqa.selenium.print;

import java.util.HashMap;
import java.util.Map;

public class PageSize {

  private final double height;
  private final double width;

    // Default Constructor (A4 by default)
    public PageSize() {
        this(PaperSize.A4); // Delegate to predefined size constructor
    }

    // Custom Size Constructor
    public PageSize(double height, double width) {
        this.height = height;
        this.width = width;
    }

    // Constructor for Predefined Sizes A4,A6,LEGAL,TABLOID using PaperSize Enum
    public PageSize(PaperSize paperSize) {
        this(paperSize.getHeight(), paperSize.getWidth()); // Delegate to custom size constructor
    }

    // Factory Methods for Predefined Sizes
    public static PageSize A4() {
        return new PageSize(PaperSize.A4);
    }

    public static PageSize A6() {
        return new PageSize(PaperSize.A6);
    }

    public static PageSize LEGAL() {
        return new PageSize(PaperSize.LEGAL);
    }

    public static PageSize TABLOID() {
        return new PageSize(PaperSize.TABLOID);
    }

    // Getters for Height and Width
    public double getHeight() {
        return height;
    }

    public double getWidth() {
        return width;
    }

    // Convert to Map (for serialization or configuration)
    public Map<String, Object> toMap() {
        final Map<String, Object> options = new HashMap<>();
        options.put("height", getHeight());
        options.put("width", getWidth());
        return options;
    }

    // Enum for Predefined Sizes
    public enum PaperSize {
        A4(27.94, 21.59),
        A6(14.8, 10.5),
        LEGAL(35.56, 21.59),
        TABLOID(43.18, 27.94);

        private final double height;
        private final double width;

        PaperSize(double height, double width) {
            this.height = height;
            this.width = width;
        }

        public double getHeight() {
            return height;
        }

        public double getWidth() {
            return width;
        }
    }

    @Override
    public String toString() {
    return String.format("PageSize[height=%.2f, width=%.2f]", height, width);
}

}
