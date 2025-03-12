// <copyright file="CallFunctionLocalValueTest.cs" company="Selenium Committers">
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
// </copyright>

using NUnit.Framework;
using OpenQA.Selenium.BiDi.Modules.Script;

namespace OpenQA.Selenium.BiDi.Script;

class CallFunctionLocalValueTest : BiDiTestFixture
{
    [Test]
    public void CanCallFunctionWithArgumentUndefined()
    {
        var undefined = new LocalValue.Undefined();
        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (typeof arg !== 'undefined') {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [undefined] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentNull()
    {
        var @null = new LocalValue.Null();
        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg !== null) {
              throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [@null] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentEmptyString()
    {
        var empty = new LocalValue.String(string.Empty);
        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg !== '') {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [empty] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentNonEmptyString()
    {
        var whoaString = new LocalValue.String("whoa");
        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg !== 'whoa') {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [whoaString] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentRecentDate()
    {
        const string PinnedDateTimeString = "2025-03-09T00:30:33.083Z";

        var date = new LocalValue.Date(PinnedDateTimeString);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg.toISOString() !== '{{PinnedDateTimeString}}') {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [date] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentEpochDate()
    {
        const string EpochString = "1970-01-01T00:00:00.000Z";

        var epochDate = new LocalValue.Date(EpochString);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg.toISOString() !== '{{EpochString}}') {
                throw new Error("Assert failed: " + arg.toISOString());
              }
            }
            """, false, new() { Arguments = [epochDate] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentNumber5()
    {
        var number5 = new LocalValue.Number(5);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg !== 5) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [number5] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentNumberNegative5()
    {
        var numberMinus5 = new LocalValue.Number(-5);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg !== -5) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [numberMinus5] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentNumber0()
    {
        var number0 = new LocalValue.Number(0);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg !== 0) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [number0] });
        }, Throws.Nothing);
    }

    [Test]
    [IgnoreBrowser(Selenium.Browser.Edge, "Chromium can't handle -0 argument as a number: https://github.com/w3c/webdriver-bidi/issues/887")]
    [IgnoreBrowser(Selenium.Browser.Chrome, "Chromium can't handle -0 argument as a number: https://github.com/w3c/webdriver-bidi/issues/887")]
    public void CanCallFunctionWithArgumentNumberNegative0()
    {
        var minus0 = new LocalValue.Number(double.NegativeZero);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg !== 0 || arg.toLocaleString()[0] !== '-') {
                throw new Error("Assert failed: " + arg.toLocaleString());
              }
            }
            """, false, new() { Arguments = [minus0] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentNumberPositiveInfinity()
    {
        var infinity = new LocalValue.Number(double.PositiveInfinity);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg !== Number.POSITIVE_INFINITY) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [infinity] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentNumberNegativeInfinity()
    {
        var minusInfinity = new LocalValue.Number(double.NegativeInfinity);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg !== Number.NEGATIVE_INFINITY) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [minusInfinity] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentNumberNaN()
    {
        var nan = new LocalValue.Number(double.NaN);
        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (!isNaN(arg)) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [nan] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentRegExp()
    {
        var regex = new LocalValue.RegExp(new LocalValue.RegExp.RegExpValue("foo*") { Flags = "g" });

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (!arg.test('foo') || arg.source !== 'foo*' || !arg.global) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [regex] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentArray()
    {
        var hiString = new LocalValue.Array([new LocalValue.String("hi")]);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg.length !== 1 || arg[0] !== 'hi') {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [hiString] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentObject()
    {
        var obj = new LocalValue.Object([[new LocalValue.String("objKey"), new LocalValue.String("objValue")]]);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg.objKey !== 'objValue' || Object.keys(arg).length !== 1) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [obj] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentMap()
    {
        var arg = new LocalValue.Map([[new LocalValue.String("mapKey"), new LocalValue.String("mapValue")]]);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (arg.get('mapKey') !== 'mapValue' || arg.size !== 1) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [arg] });
        }, Throws.Nothing);
    }

    [Test]
    public void CanCallFunctionWithArgumentSet()
    {
        var argument = new LocalValue.Set([new LocalValue.String("setKey")]);

        Assert.That(async () =>
        {
            await context.Script.CallFunctionAsync($$"""
            (arg) => {
              if (!arg.has('setKey') || arg.size !== 1) {
                throw new Error("Assert failed: " + arg);
              }
            }
            """, false, new() { Arguments = [argument] });
        }, Throws.Nothing);
    }
}
