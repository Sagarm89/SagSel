# frozen_string_literal: true

# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

module Selenium
  module WebDriver
    class BiDi
      class SetCookieHeaders
        def initialize(set_cookie_headers = {})
          @set_cookie_headers = set_cookie_headers
        end

        def all
          @set_cookie_headers
        end

        def []=(key, value)
          @set_cookie_headers[key] = {value: value}
        end

        def [](key)
          @set_cookie_headers[key]
        end

        def delete(key)
          @set_cookie_headers.delete(key)
        end

        def serialize
          return [] unless @set_cookie_headers

          @set_cookie_headers.map do |name, data|
            data = {value: data} unless data.is_a?(Hash)

            {
              name: name.to_s,
              value: {
                type: 'string',
                value: data[:value].to_s
              },
              domain: data[:domain],
              httpOnly: data[:httpOnly],
              expiry: data[:expiry],
              maxAge: data[:maxAge],
              path: data[:path],
              sameSite: data[:sameSite],
              secure: data[:secure]
            }.compact
          end
        end
      end
    end # BiDi
  end # WebDriver
end # Selenium
